# remover torneios incompletos do banco de dados
# útil caso acidentalmente o script de update_tournaments salve um torneio antes dele terminar.

import sqlite3
import os
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

# 1. MÁGICA DOS CAMINHOS: O script descobre onde ele está e acha a raiz do projeto
# __file__ aponta para tools/unblock_tournament.py
# Subindo um nível com dirname, chegamos na raiz do projeto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 2. Constrói o caminho absoluto para o banco de dados
DB_FILE = os.path.join(BASE_DIR, "data", "team_users.db")

# 3. Verifica se o usuário passou o ID no terminal
if len(sys.argv) < 2:
    print("❌ Erro: Você esqueceu de informar o ID do torneio.")
    print("Uso correto: python tools/unblock_tournament.py <ID_DO_TORNEIO>")
    sys.exit(1)

# Pega o ID passado no comando
TID_ERRADO = sys.argv[1].strip()

# 4. Executa a limpeza
if os.path.exists(DB_FILE):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    
    # Remove o torneio e os resultados associados a ele
    cur.execute("DELETE FROM tournament_results WHERE tournament_id = ?", (TID_ERRADO,))
    cur.execute("DELETE FROM tournaments WHERE tournament_id = ?", (TID_ERRADO,))
    
    linhas_afetadas = cur.rowcount
    
    conn.commit()
    conn.close()
    
    if linhas_afetadas > 0:
        print(f"✅ Torneio '{TID_ERRADO}' removido com sucesso do banco local!")
        print("   -> Agora você pode rodar o update_tournaments.py novamente.")
    else:
        print(f"⚠️ O torneio '{TID_ERRADO}' não foi encontrado no banco de dados local.")
else:
    print(f"❌ Banco de dados não encontrado no caminho:\n{DB_FILE}")