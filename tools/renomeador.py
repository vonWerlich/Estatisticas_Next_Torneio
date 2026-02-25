import json
import sqlite3
import os
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

# Lógica para achar o banco de dados, não importa de onde você rode o script
DIR_ATUAL = os.path.dirname(os.path.abspath(__file__))
RAIZ_DO_PROJETO = os.path.dirname(DIR_ATUAL)
DB_FILE = os.path.join(RAIZ_DO_PROJETO, "data", "team_users.db")

def atualizar_json_backup(cursor, raiz):
    """Lê o estado atual do banco e atualiza o JSON de backup."""
    cursor.execute("SELECT tournament_id, circuito FROM tournaments WHERE circuito IS NOT NULL AND circuito != ''")
    mapeamento = {row[0]: row[1] for row in cursor.fetchall()}
    
    caminho_json = os.path.join(raiz, "data", "circuitos_map.json")
    with open(caminho_json, "w", encoding="utf-8") as f:
        json.dump(mapeamento, f, ensure_ascii=False, indent=2)

def renomear_circuitos():
    if not os.path.exists(DB_FILE):
        print(f"❌ Banco de dados não encontrado em: {DB_FILE}")
        return

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Pega todos os nomes únicos de circuitos que já existem no banco
    cursor.execute("""
        SELECT DISTINCT circuito 
        FROM tournaments 
        WHERE circuito IS NOT NULL AND circuito != '' AND circuito != 'Ignorado'
        ORDER BY circuito
    """)
    circuitos_atuais = [row[0] for row in cursor.fetchall()]

    if not circuitos_atuais:
        print("Nenhum circuito classificado encontrado para renomear.")
        conn.close()
        return

    print("🏷️ CIRCUITOS ATUAIS NO BANCO:")
    for c in circuitos_atuais:
        print(f" - {c}")
    print("-" * 40)

    while True:
        print("\n(Digite 'sair' a qualquer momento para encerrar)")
        nome_antigo = input("👉 Qual nome você quer MUDAR? (ex: Quarentena 2020): ").strip()
        
        if nome_antigo.lower() == 'sair':
            break
            
        if nome_antigo not in circuitos_atuais:
            print("❌ Esse nome não existe no banco. Digite exatamente como aparece na lista acima.")
            continue
            
        nome_novo = input(f"👉 Qual será o NOVO nome para '{nome_antigo}'? (ex: 2020 Quarentena): ").strip()
        
        if nome_novo.lower() == 'sair':
            break

        # Faz a atualização em lote (todos os torneios com o nome antigo recebem o novo)
        cursor.execute("UPDATE tournaments SET circuito = ? WHERE circuito = ?", (nome_novo, nome_antigo))
        conn.commit()
        atualizar_json_backup(cursor, RAIZ_DO_PROJETO)
        
        linhas_afetadas = cursor.rowcount
        print(f"✅ Sucesso! {linhas_afetadas} torneios foram renomeados de '{nome_antigo}' para '{nome_novo}'.")
        
        # Atualiza a lista interna para não mostrar o nome antigo de novo
        circuitos_atuais.remove(nome_antigo)
        if nome_novo not in circuitos_atuais:
            circuitos_atuais.append(nome_novo)
            circuitos_atuais.sort()

    conn.close()
    print("🏁 Renomeação finalizada!")

if __name__ == "__main__":
    renomear_circuitos()