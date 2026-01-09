import sqlite3
import json
import glob
import os
import requests
import time
from datetime import datetime
import sys

# Ajuste de encoding para Windows
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

# ================= CONFIGURAÇÃO =================

DB_FILE = "team_users.db"

# Headers para a API
HEADERS = {
    "User-Agent": "HistoryFixerBot/1.1 (Kauan/TeamManager)",
    "Accept": "application/json"
}

# ================= FUNÇÕES DE ARQUIVO =================

def get_tournament_dir():
    """Tenta adivinhar o nome da pasta de torneios"""
    candidates = ["torneiosnew", "torneios_new", "torneios"]
    for d in candidates:
        if os.path.exists(d) and os.path.isdir(d):
            print(f"📂 Pasta de torneios encontrada: '{d}'")
            return d
    
    print("❌ ERRO CRÍTICO: Nenhuma pasta de torneios encontrada!")
    print(f"   Procurei por: {candidates}")
    print("   Certifique-se que a pasta existe no mesmo local deste script.")
    return None

def parse_iso_date(timestamp_ms_or_str):
    try:
        if isinstance(timestamp_ms_or_str, int):
            dt = datetime.fromtimestamp(timestamp_ms_or_str / 1000)
            return dt.strftime("%Y-%m-%d")
        else:
            dt = datetime.fromisoformat(timestamp_ms_or_str.replace("Z", "+00:00"))
            return dt.strftime("%Y-%m-%d")
    except Exception:
        return None

def scan_local_files(directory):
    print(f"🕵️ Iniciando varredura em: {directory}")
    users_found = {}
    
    folders = glob.glob(os.path.join(directory, "*"))
    print(f"   Encontradas {len(folders)} pastas de torneios.")

    if len(folders) == 0:
        print("⚠️ AVISO: A pasta existe mas parece vazia! Verifique se os torneios estão dentro.")
        return {}

    for folder in folders:
        info_path = os.path.join(folder, "info.json")
        games_path = os.path.join(folder, "games.ndjson")
        
        if not os.path.exists(info_path) or not os.path.exists(games_path):
            continue

        # Data do Torneio
        tourney_date = None
        try:
            with open(info_path, "r", encoding="utf-8") as f:
                info = json.load(f)
                raw_date = info.get("startsAt") or info.get("date")
                tourney_date = parse_iso_date(raw_date)
        except Exception:
            pass

        if not tourney_date:
            continue

        # Jogadores
        try:
            with open(games_path, "r", encoding="utf-8") as f:
                for line in f:
                    if not line.strip(): continue
                    game = json.loads(line)
                    
                    for color in ['white', 'black']:
                        player_data = game.get("players", {}).get(color, {}).get("user")
                        if player_data:
                            uid = player_data.get("id", "").lower()
                            uname = player_data.get("name", "")
                            
                            if uid:
                                if uid not in users_found:
                                    users_found[uid] = {'username': uname, 'dates': set()}
                                users_found[uid]['dates'].add(tourney_date)
        except Exception:
            pass

    print(f"✅ Varredura concluída. {len(users_found)} jogadores únicos encontrados.")
    return users_found

# ================= FUNÇÕES DE API E DB =================

def extract_ratings_full(user_obj):
    perfs = user_obj.get("perfs", {})
    return (
        perfs.get("bullet", {}).get("rating"),
        perfs.get("blitz", {}).get("rating"),
        perfs.get("rapid", {}).get("rating"),
        perfs.get("classical", {}).get("rating"),
        perfs.get("correspondence", {}).get("rating"),
        perfs.get("crazyhouse", {}).get("rating"),
        perfs.get("chess960", {}).get("rating"),
        perfs.get("kingOfTheHill", {}).get("rating"),
        perfs.get("threeCheck", {}).get("rating"),
        perfs.get("antichess", {}).get("rating"),
        perfs.get("atomic", {}).get("rating"),
        perfs.get("horde", {}).get("rating"),
        perfs.get("racingKings", {}).get("rating"),
        perfs.get("ultraBullet", {}).get("rating"),
        perfs.get("puzzle", {}).get("rating")
    )

def extract_stats(user_obj):
    count = user_obj.get("count", {})
    return (
        count.get("all"), count.get("win"), count.get("loss"), count.get("draw"),
        user_obj.get("playTime", {}).get("total")
    )

def chunk_list(lst, size):
    for i in range(0, len(lst), size):
        yield lst[i:i + size]

def fetch_and_update_db(users_map):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    
    all_ids = list(users_map.keys())
    
    # FASE 1: BULK (Ativos)
    print("🚀 Buscando dados na API (Bulk)...")
    returned_ids = set()
    
    for batch in chunk_list(all_ids, 300):
        try:
            r = requests.post("https://lichess.org/api/users", data=",".join(batch), headers=HEADERS)
            if r.status_code == 200:
                api_data = r.json()
                for u in api_data:
                    uid = u.get("id", "").lower()
                    returned_ids.add(uid)
                    
                    local = users_map.get(uid)
                    sorted_dates = sorted(list(local['dates']))
                    
                    if u.get("disabled"): status = "closed"
                    elif u.get("tosViolation"): status = "banned"
                    else: status = "active" if u.get("seenAt") else "inactive"

                    ratings = extract_ratings_full(u)
                    stats = extract_stats(u)
                    
                    cur.execute("""
                        INSERT INTO users (
                            id_lichess, username, status, is_team_member, 
                            country, bio,
                            rating_bullet, rating_blitz, rating_rapid, rating_classical, rating_correspondence,
                            rating_crazyhouse, rating_chess960, rating_king_of_the_hill, rating_three_check,
                            rating_antichess, rating_atomic, rating_horde, rating_racing_kings, rating_ultra_bullet, rating_puzzle,
                            total_games, total_wins, total_losses, total_draws, play_time_total,
                            created_at, seen_at, last_seen_api_timestamp,
                            first_seen_team_date, last_seen_team_date, raw_json
                        ) VALUES (?,?,?,0,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                        ON CONFLICT(id_lichess) DO UPDATE SET
                            username=excluded.username, status=excluded.status,
                            rating_blitz=excluded.rating_blitz, rating_rapid=excluded.rating_rapid,
                            first_seen_team_date=excluded.first_seen_team_date,
                            last_seen_team_date=excluded.last_seen_team_date,
                            raw_json=excluded.raw_json
                    """, (
                        uid, u.get("username"), status, 
                        u.get("profile", {}).get("country"), u.get("profile", {}).get("bio"),
                        *ratings, *stats,
                        u.get("createdAt"), u.get("seenAt"), int(time.time()*1000),
                        sorted_dates[0], sorted_dates[-1], json.dumps(u)
                    ))
                conn.commit()
                time.sleep(1)
        except Exception as e:
            print(f"Erro no lote: {e}")

    # FASE 2: FANTASMAS (Banidos/Closed)
    missing = [uid for uid in all_ids if uid not in returned_ids]
    print(f"🕵️ Processando {len(missing)} contas ausentes/fechadas...")
    
    for i, uid in enumerate(missing):
        local = users_map.get(uid)
        sorted_dates = sorted(list(local['dates']))
        
        try:
            r = requests.get(f"https://lichess.org/api/user/{uid}", headers=HEADERS)
            status = "closed" if r.status_code == 404 else "unknown"
            raw_data = "{}"
            
            if r.status_code == 200:
                data = r.json()
                raw_data = json.dumps(data)
                if data.get("disabled"): status = "closed"
                elif data.get("tosViolation"): status = "banned"
                else: status = "active"

            cur.execute("""
                INSERT INTO users (
                    id_lichess, username, status, is_team_member,
                    first_seen_team_date, last_seen_team_date, raw_json, last_seen_api_timestamp
                ) VALUES (?, ?, ?, 0, ?, ?, ?, ?)
                ON CONFLICT(id_lichess) DO UPDATE SET
                    status=excluded.status,
                    first_seen_team_date=excluded.first_seen_team_date,
                    last_seen_team_date=excluded.last_seen_team_date
            """, (uid, local['username'], status, sorted_dates[0], sorted_dates[-1], raw_data, int(time.time()*1000)))
            
            if i % 10 == 0: conn.commit()
            time.sleep(0.7)
            
        except Exception:
            pass

    conn.commit()
    conn.close()
    print("✅ Banco de dados preenchido com sucesso!")

if __name__ == "__main__":
    if not os.path.exists(DB_FILE):
        print("❌ Banco de dados não existe. Rode init_db.py primeiro!")
    else:
        d = get_tournament_dir()
        if d:
            users = scan_local_files(d)
            if users:
                fetch_and_update_db(users)
            else:
                print("❌ Nenhum usuário encontrado nos arquivos.")