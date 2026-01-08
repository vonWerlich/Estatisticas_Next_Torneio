import requests
import json
import os
import sys

# --- CONFIGURAÇÃO ---
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

TEAM_ID = "next-nucleo-de-estudos-em-xadrez--tecnologias"
DATA_DIR_PLAYERS = "player_data"
PLAYER_DB_FILE = os.path.join(DATA_DIR_PLAYERS, "players.json")
OUTPUT_FILE = os.path.join(DATA_DIR_PLAYERS, "ex_members.json")

def carregar_json(filepath):
    if not os.path.exists(filepath): return []
    try:
        with open(filepath, "r", encoding="utf-8") as f: return json.load(f)
    except: return []

def salvar_json(filepath, data):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def main():
    print(f"--- DETETIVE DE EX-MEMBROS ---")
    
    # 1. Carregar DB Local (Quem já jogou)
    players_db = carregar_json(PLAYER_DB_FILE)
    # Mapa: ID -> Dados Completos
    local_players_map = {}
    for p in players_db:
        if p.get('username'):
            # Usa lower() para garantir match
            local_players_map[p['username'].lower()] = p

    print(f"📂 Histórico local: {len(local_players_map)} jogadores.")
    
    # 2. Baixar lista ATUAL da equipe (API)
    print(f"📡 Baixando lista atual da equipe '{TEAM_ID}'...")
    url = f"https://lichess.org/api/team/{TEAM_ID}/users"
    
    current_team_ids = set()
    
    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            for line in r.iter_lines():
                if line:
                    data = json.loads(line.decode('utf-8'))
                    # Pega ID ou Username e normaliza para lower
                    uid = data.get("id")
                    if not uid: uid = data.get("username", "").lower()
                    current_team_ids.add(uid)
                        
    except Exception as e:
        print(f"❌ Erro ao baixar membros: {e}")
        return

    print(f"👥 Membros atuais na equipe: {len(current_team_ids)}")

    # 3. O Pulo do Gato: Quem está no DB mas NÃO está na equipe?
    ex_members_list = []
    
    for pid, p_data in local_players_map.items():
        if pid not in current_team_ids:
            # Achamos um ex-membro!
            ex_members_list.append({
                "username": p_data["username"],
                "status_db": p_data.get("status"), # Provavelmente 'active' ou 'closed'
                "last_seen_team": p_data.get("last_seen_team_date")
            })

    # 4. Relatório
    print(f"\n🔍 Resultado da Análise:")
    print(f"   - Ex-membros encontrados: {len(ex_members_list)}")
    
    if ex_members_list:
        salvar_json(OUTPUT_FILE, ex_members_list)
        print(f"✅ Lista salva em: {OUTPUT_FILE}")
        
        # Análise rápida dos status
        closed_cnt = sum(1 for x in ex_members_list if x['status_db'] == 'closed')
        banned_cnt = sum(1 for x in ex_members_list if x['status_db'] == 'banned')
        print(f"   - Desses, {closed_cnt} constam como 'closed' no seu DB.")
        print(f"   - Desses, {banned_cnt} constam como 'banned' no seu DB.")
        print(f"   - Os outros {len(ex_members_list) - closed_cnt - banned_cnt} saíram voluntariamente.")

if __name__ == "__main__":
    main()