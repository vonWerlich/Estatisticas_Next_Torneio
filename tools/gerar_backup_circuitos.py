import sqlite3
import os
import json
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

DIR_ATUAL = os.path.dirname(os.path.abspath(__file__))
RAIZ_DO_PROJETO = os.path.dirname(DIR_ATUAL)
DB_FILE = os.path.join(RAIZ_DO_PROJETO, "data", "team_users.db")
BACKUP_FILE = os.path.join(RAIZ_DO_PROJETO, "data", "circuitos_map.json")

def fazer_backup():
    if not os.path.exists(DB_FILE):
        print("❌ Banco não encontrado!")
        return

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Pega apenas os torneios que têm um circuito válido
    cursor.execute("""
        SELECT tournament_id, circuito 
        FROM tournaments 
        WHERE circuito IS NOT NULL AND circuito != ''
    """)
    
    # Transforma o resultado do banco num dicionário {id: circuito}
    mapeamento = {row[0]: row[1] for row in cursor.fetchall()}
    conn.close()

    # Salva o dicionário no arquivo JSON
    with open(BACKUP_FILE, "w", encoding="utf-8") as f:
        json.dump(mapeamento, f, ensure_ascii=False, indent=2)

    print(f"✅ Backup criado com sucesso em 'data/circuitos_map.json'!")
    print(f"💾 Total de torneios salvos: {len(mapeamento)}")

if __name__ == "__main__":
    fazer_backup()