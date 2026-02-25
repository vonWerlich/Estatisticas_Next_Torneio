import json
import sqlite3
import os
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

# Localiza o banco de dados magicamente
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

def corrigir_torneio_individual():
    if not os.path.exists(DB_FILE):
        print(f"❌ Banco de dados não encontrado em: {DB_FILE}")
        return

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    print("🚑 BEM-VINDO AO CORRETOR CIRÚRGICO DE TORNEIOS")
    
    while True:
        print("\n" + "="*60)
        busca = input("🔍 Digite parte do NOME ou ID do torneio (ou 'sair'): ").strip()
        
        if busca.lower() == 'sair':
            break
            
        if not busca:
            continue

        # Busca no banco por nome do torneio ou ID do Lichess
        cursor.execute("""
            SELECT tournament_id, tournament_start_datetime, tournament_name, circuito 
            FROM tournaments 
            WHERE tournament_name LIKE ? OR tournament_id LIKE ?
            ORDER BY tournament_start_datetime DESC
            LIMIT 10
        """, (f"%{busca}%", f"%{busca}%"))
        
        resultados = cursor.fetchall()
        
        if not resultados:
            print("❌ Nenhum torneio encontrado com esse termo.")
            continue
            
        print(f"\n📋 Encontramos {len(resultados)} torneio(s) (mostrando até 10):")
        for tid, data, nome, circuito in resultados:
            data_curta = data.split("T")[0] if data else "????"
            circ_atual = circuito if circuito else "NÃO CLASSIFICADO (Vazio)"
            print(f"ID: [{tid}] | 📅 {data_curta} | 🏆 {nome}")
            print(f"    👉 Circuito atual: {circ_atual}\n")
            
        print("-" * 60)
        tid_escolhido = input("🎯 Cole o ID do torneio que quer corrigir (ou Enter para nova busca): ").strip()
        
        if not tid_escolhido:
            continue
            
        # Verifica se o ID digitado realmente apareceu na busca para evitar erros
        ids_encontrados = [r[0] for r in resultados]
        if tid_escolhido not in ids_encontrados:
            print("❌ ID inválido. Cole exatamente o texto que está entre colchetes [ ].")
            continue
            
        novo_circuito = input(f"✍️ Novo nome do circuito para '{tid_escolhido}' (ou 'p' p/ esvaziar, 'i' p/ ignorar): ").strip()
        
        if novo_circuito.lower() == 'p' or novo_circuito == '':
            cursor.execute("UPDATE tournaments SET circuito = NULL WHERE tournament_id = ?", (tid_escolhido,))
            acao = "ESVAZIADO (Voltará para a fila do classificador.py)"
        elif novo_circuito.lower() == 'i':
            cursor.execute("UPDATE tournaments SET circuito = 'Ignorado' WHERE tournament_id = ?", (tid_escolhido,))
            acao = "marcado como IGNORADO"
        else:
            cursor.execute("UPDATE tournaments SET circuito = ? WHERE tournament_id = ?", (novo_circuito, tid_escolhido))
            acao = f"reclassificado como '{novo_circuito}'"
            
        conn.commit()
        atualizar_json_backup(cursor, RAIZ_DO_PROJETO)
        print(f"✅ Sucesso! O torneio [{tid_escolhido}] foi {acao}.")

    conn.close()
    print("🏁 Correção finalizada!")

if __name__ == "__main__":
    corrigir_torneio_individual()