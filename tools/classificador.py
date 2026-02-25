import json
import sqlite3
import os
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

# 1. Pega o caminho absoluto da pasta onde este script está salvo (ex: /scripts/)
DIR_ATUAL = os.path.dirname(os.path.abspath(__file__))

# 2. Sobe um "andar" para chegar na raiz do projeto
RAIZ_DO_PROJETO = os.path.dirname(DIR_ATUAL)

# 3. Monta o caminho exato para o banco de dados
DB_FILE = os.path.join(RAIZ_DO_PROJETO, "data", "team_users.db")

def atualizar_json_backup(cursor, raiz):
    """Lê o estado atual do banco e atualiza o JSON de backup."""
    cursor.execute("SELECT tournament_id, circuito FROM tournaments WHERE circuito IS NOT NULL AND circuito != ''")
    mapeamento = {row[0]: row[1] for row in cursor.fetchall()}
    
    caminho_json = os.path.join(raiz, "data", "circuitos_map.json")
    with open(caminho_json, "w", encoding="utf-8") as f:
        json.dump(mapeamento, f, ensure_ascii=False, indent=2)

def classificar_torneios_pendentes():
    if not os.path.exists(DB_FILE):
        print(f"❌ Banco de dados não encontrado em: {DB_FILE}")
        return

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Busca torneios que AINDA NÃO têm circuito definido (NULL ou vazio)
    cursor.execute("""
        SELECT tournament_id, tournament_start_datetime, tournament_name, tournament_system 
        FROM tournaments 
        WHERE circuito IS NULL OR circuito = ''
        ORDER BY tournament_start_datetime ASC
    """)
    torneios_pendentes = cursor.fetchall()

    if not torneios_pendentes:
        print("🎉 Que maravilha! Todos os torneios já estão classificados!")
        conn.close()
        return

    print(f"🔍 Encontrados {len(torneios_pendentes)} torneios aguardando classificação.\n")
    print("📋 INSTRUÇÕES:")
    print(" - Digite o NOME DO CIRCUITO (ex: 2024-1) para classificar.")
    print(" - Digite 'i' para IGNORAR definitivamente (não entra em circuitos).")
    print(" - Digite 'p' (ou aperte Enter) para PULAR por enquanto.")
    print(" - Digite 'sair' para encerrar o script.\n")

    for tid, data, nome, sistema in torneios_pendentes:
        data_curta = data.split("T")[0] if data else "Data Desconhecida"
        
        if sistema == 'swiss':
            url_lichess = f"https://lichess.org/swiss/{tid}"
        else:
            url_lichess = f"https://lichess.org/tournament/{tid}"
        
        print("=" * 60)
        print(f"🏆 {nome}")
        print(f"📅 Data: {data_curta} | ⚙️ Sistema: {str(sistema).upper()}")
        print(f"🔗 Link: {url_lichess}")
        
        resposta = input("👉 Qual nome deseja colocar aqui? ").strip()

        if resposta.lower() == 'sair':
            print("💾 Salvando progresso e saindo...")
            break
        elif resposta.lower() == 'p' or resposta == '':
            print("⏭️ Pulando... (Ficará para a próxima)")
            continue
        elif resposta.lower() == 'i':
            cursor.execute("UPDATE tournaments SET circuito = 'Ignorado' WHERE tournament_id = ?", (tid,))
            conn.commit()
            atualizar_json_backup(cursor, RAIZ_DO_PROJETO)
            print("🚫 Marcado como Ignorado!")
        else:
            cursor.execute("UPDATE tournaments SET circuito = ? WHERE tournament_id = ?", (resposta, tid))
            conn.commit()
            atualizar_json_backup(cursor, RAIZ_DO_PROJETO)
            print(f"✅ Classificado com sucesso como '{resposta}'!")

    conn.close()
    print("\n🏁 Sessão de classificação finalizada!")

if __name__ == "__main__":
    classificar_torneios_pendentes()