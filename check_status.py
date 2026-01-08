import os
import requests
import json
import time
import sys
from datetime import datetime, timedelta, timezone

# --- CONFIGURAÇÃO ---
DATA_DIR_PLAYERS = "player_data"
PLAYER_DB_FILE = os.path.join(DATA_DIR_PLAYERS, "players.json")
BANNED_PLAYERS_FILE = os.path.join(DATA_DIR_PLAYERS, "banned_players.json")
INACTIVE_PLAYERS_FILE = os.path.join(DATA_DIR_PLAYERS, "inactive_players.json")
STATUS_METADATA_FILE = os.path.join(DATA_DIR_PLAYERS, "status_metadata.json")

TEAM_INACTIVITY_DAYS = 547
LICHESS_API_PAUSE = 1.1

def carregar_json(filepath, default_value):
    if not os.path.exists(filepath): return default_value
    try:
        with open(filepath, "r", encoding="utf-8") as f: return json.load(f)
    except: return default_value

def salvar_json(filepath, data):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def run_status_check():
    print("--- VERIFICAÇÃO MENSAL DE STATUS (BANIDOS/INATIVOS) ---")
    
    players_db = carregar_json(PLAYER_DB_FILE, [])
    if not players_db:
        print("⚠ DB vazio.")
        return

    banned_list = []
    inactive_list = []
    now = datetime.now(timezone.utc)
    inactivity_limit = timedelta(days=TEAM_INACTIVITY_DAYS)
    
    print(f"🕵️ Analisando {len(players_db)} jogadores...")
    
    count = 0
    for p in players_db:
        username = p["username"]
        status = p.get("status", "active")
        
        # 1. API Check (Ban/Closed) - Pula se já soubermos que está banido
        if status != "banned":
            try:
                r = requests.get(f"https://lichess.org/api/user/{username}")
                time.sleep(LICHESS_API_PAUSE) # Respeita a API
                
                if r.status_code == 200:
                    data = r.json()
                    p["last_seen_api_timestamp"] = data.get("seenAt")
                    
                    if data.get("tosViolation"):
                        p["status"] = "banned"
                        print(f"🚫 {username} -> BANIDO")
                    elif data.get("disabled"):
                        p["status"] = "closed"
                    elif status == "closed":
                        p["status"] = "active" # Reabriu
                        
                elif r.status_code == 404:
                    if status != "closed": p["status"] = "closed"
            except Exception as e:
                print(f"⚠ Erro em {username}: {e}")

        # 2. Inactivity Check
        # (Lógica idêntica ao script anterior)
        if p.get("status") not in ["banned", "closed"]:
            ls_str = p.get("last_seen_team_date")
            if ls_str:
                try:
                    ls_dt = datetime.fromisoformat(ls_str.replace('Z', '+00:00'))
                    if (now - ls_dt) > inactivity_limit:
                        p["status"] = "inactive"
                except: pass

        # Popula listas auxiliares
        final_status = p.get("status")
        if final_status == "banned": banned_list.append(username)
        if final_status == "inactive": inactive_list.append(username)
        
        count += 1
        if count % 50 == 0: print(f"  ...processados {count}/{len(players_db)}")

    print("💾 Salvando atualizações...")
    salvar_json(PLAYER_DB_FILE, players_db)
    salvar_json(BANNED_PLAYERS_FILE, banned_list)
    salvar_json(INACTIVE_PLAYERS_FILE, inactive_list)
    salvar_json(STATUS_METADATA_FILE, {"last_full_check": now.isoformat()})
    print("✅ Verificação mensal concluída.")

if __name__ == "__main__":
    run_status_check()