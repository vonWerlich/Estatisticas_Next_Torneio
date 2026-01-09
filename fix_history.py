import sqlite3
import json
import glob
import os
import requests
import time
from datetime import datetime

# ================= CONFIGURAÇÃO =================

# Caminho onde estão as pastas dos torneios
TOURNAMENT_DIR = "torneios_new" 
DB_FILE = "team_users.db"

# Headers para a API (Respeitando boas práticas)
HEADERS = {
    "User-Agent": "HistoryFixerBot/1.0 (Kauan/TeamManager)",
    "Accept": "application/json"
}

# ================= FUNÇÕES DE ARQUIVO =================

def parse_iso_date(timestamp_ms_or_str):
    """Converte timestamp ou string ISO para YYYY-MM-DD"""
    try:
        if isinstance(timestamp_ms_or_str, int):
            dt = datetime.fromtimestamp(timestamp_ms_or_str / 1000)
            return dt.strftime("%Y-%m-%d")
        else:
            # Tenta parsear string ISO (ex: 2023-01-01T14:00:00Z)
            dt = datetime.fromisoformat(timestamp_ms_or_str.replace("Z", "+00:00"))
            return dt.strftime("%Y-%m-%d")
    except Exception:
        return None

def scan_local_files():
    """
    Lê todos os torneios e retorna um dicionário:
    {
        'user_id': {
            'username': 'NomeOriginal',
            'dates': {'2023-01-01', '2023-02-15', ...} (Set para evitar duplicatas)
        }
    }
    """
    print(f"📂 Iniciando varredura em: {TOURNAMENT_DIR}")
    users_found = {}
    
    # Procura todas as pastas dentro de torneios_new
    folders = glob.glob(os.path.join(TOURNAMENT_DIR, "*"))
    print(f"   Encontradas {len(folders)} pastas de torneios.")

    for folder in folders:
        # 1. Pegar a Data do Torneio (info.json)
        info_path = os.path.join(folder, "info.json")
        games_path = os.path.join(folder, "games.ndjson")
        
        if not os.path.exists(info_path) or not os.path.exists(games_path):
            continue

        try:
            with open(info_path, "r", encoding="utf-8") as f:
                info = json.load(f)
                # Tenta pegar startsAt (timestamp) ou date (string)
                raw_date = info.get("startsAt") or info.get("date")
                tourney_date = parse_iso_date(raw_date)
                
                if not tourney_date:
                    print(f"⚠️ Data inválida em {folder}")
                    continue
        except Exception as e:
            print(f"❌ Erro lendo info em {folder}: {e}")
            continue

        # 2. Ler Jogadores dos Games (games.ndjson)
        # Isso pega TODO MUNDO, inclusive banidos que não aparecem no results.json
        try:
            with open(games_path, "r", encoding="utf-8") as f:
                for line in f:
                    if not line.strip(): continue
                    game = json.loads(line)
                    
                    # Processa White e Black
                    for color in ['white', 'black']:
                        player_data = game.get("players", {}).get(color, {}).get("user")
                        if player_data:
                            uid = player_data.get("id", "").lower() # Normaliza ID
                            uname = player_data.get("name", "")
                            
                            if uid:
                                if uid not in users_found:
                                    users_found[uid] = {
                                        'username': uname,
                                        'dates': set()
                                    }
                                users_found[uid]['dates'].add(tourney_date)
                                
        except Exception as e:
            print(f"❌ Erro lendo games em {folder}: {e}")

    print(f"✅ Varredura concluída. {len(users_found)} jogadores únicos encontrados no histórico.")
    return users_found

# ================= FUNÇÕES DE API E DB =================

def extract_ratings_full(user_obj):
    """Extrai todas as variantes possíveis para o novo schema"""
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
        count.get("all"),
        count.get("win"),
        count.get("loss"),
        count.get("draw"),
        user_obj.get("playTime", {}).get("total")
    )

def chunk_list(lst, size):
    for i in range(0, len(lst), size):
        yield lst[i:i + size]

def fetch_and_update_db(users_map):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    
    all_ids = list(users_map.keys())
    total = len(all_ids)
    processed_count = 0
    
    print("🚀 Iniciando atualização via API (Ratings + Status)...")
    
    # Conjunto para rastrear quem a API retornou (para achar os banidos/fechados)
    returned_ids = set()

    # --- FASE 1: BULK CHECK (Contas ativas/normais) ---
    for batch in chunk_list(all_ids, 300):
        try:
            # Request para API
            r = requests.post("https://lichess.org/api/users", data=",".join(batch), headers=HEADERS)
            if r.status_code != 200:
                print(f"⚠️ Erro API {r.status_code}. Pulando lote...")
                continue
                
            api_data = r.json()
            
            for u in api_data:
                uid = u.get("id", "").lower()
                if not uid: continue
                
                returned_ids.add(uid)
                local_data = users_map.get(uid)
                
                # Calcula Datas
                sorted_dates = sorted(list(local_data['dates']))
                first_seen = sorted_dates[0]
                last_seen = sorted_dates[-1]

                # Status
                if u.get("disabled", False):
                    status = "closed"
                elif u.get("tosViolation", False):
                    status = "banned"
                else:
                    status = "active" if u.get("seenAt") else "inactive"

                # Ratings & Stats
                ratings = extract_ratings_full(u)
                stats = extract_stats(u)
                
                # Upsert Query (Inserir ou Atualizar)
                # OBS: raw_json salva tudo para futuro
                cur.execute("""
                    INSERT INTO users (
                        id_lichess, username, status, is_team_member, 
                        country, bio,
                        rating_bullet, rating_blitz, rating_rapid, rating_classical, rating_correspondence,
                        rating_crazyhouse, rating_chess960, rating_king_of_the_hill, rating_three_check,
                        rating_antichess, rating_atomic, rating_horde, rating_racing_kings, rating_ultra_bullet, rating_puzzle,
                        total_games, total_wins, total_losses, total_draws, play_time_total,
                        created_at, seen_at, last_seen_api_timestamp,
                        first_seen_team_date, last_seen_team_date,
                        raw_json
                    ) VALUES (
                        ?, ?, ?, ?,
                        ?, ?,
                        ?, ?, ?, ?, ?,
                        ?, ?, ?, ?,
                        ?, ?, ?, ?, ?, ?,
                        ?, ?, ?, ?, ?,
                        ?, ?, ?,
                        ?, ?,
                        ?
                    )
                    ON CONFLICT(id_lichess) DO UPDATE SET
                        username=excluded.username,
                        status=excluded.status,
                        rating_blitz=excluded.rating_blitz,
                        rating_rapid=excluded.rating_rapid,
                        rating_classical=excluded.rating_classical,
                        rating_puzzle=excluded.rating_puzzle,
                        first_seen_team_date=excluded.first_seen_team_date,
                        last_seen_team_date=excluded.last_seen_team_date,
                        raw_json=excluded.raw_json,
                        last_seen_api_timestamp=excluded.last_seen_api_timestamp
                """, (
                    uid, u.get("username"), status, 0, # is_team_member default 0
                    u.get("profile", {}).get("country"), u.get("profile", {}).get("bio"),
                    *ratings,
                    *stats,
                    u.get("createdAt"), u.get("seenAt"), int(time.time()*1000),
                    first_seen, last_seen,
                    json.dumps(u) # raw_json
                ))
            
            conn.commit()
            processed_count += len(batch)
            print(f"   Processados {processed_count}/{total} via Bulk...")
            time.sleep(1.0) # Respeita Rate Limit

        except Exception as e:
            print(f"❌ Erro crítico no lote: {e}")

    # --- FASE 2: CAÇA AOS FANTASMAS (Banidos/Closed que o Bulk escondeu) ---
    missing_ids = [uid for uid in all_ids if uid not in returned_ids]
    print(f"🕵️ Investigando {len(missing_ids)} contas fantasmas (possíveis banidos/closed)...")
    
    for i, uid in enumerate(missing_ids):
        local_data = users_map.get(uid)
        sorted_dates = sorted(list(local_data['dates']))
        
        # Verifica individualmente
        try:
            r = requests.get(f"https://lichess.org/api/user/{uid}", headers=HEADERS)
            
            status = "unknown"
            raw_data = "{}"
            
            # Se 404, a conta foi apagada completamente
            if r.status_code == 404:
                status = "closed"
            elif r.status_code == 200:
                data = r.json()
                raw_data = json.dumps(data)
                
                if data.get("disabled"): status = "closed"
                elif data.get("tosViolation"): status = "banned"
                else: status = "active" # Raro, mas pode acontecer se o bulk falhou
            
            # Insere no banco apenas com as infos básicas + datas locais
            cur.execute("""
                INSERT INTO users (
                    id_lichess, username, status, is_team_member,
                    first_seen_team_date, last_seen_team_date, raw_json, last_seen_api_timestamp
                ) VALUES (?, ?, ?, 0, ?, ?, ?, ?)
                ON CONFLICT(id_lichess) DO UPDATE SET
                    status=excluded.status,
                    first_seen_team_date=excluded.first_seen_team_date,
                    last_seen_team_date=excluded.last_seen_team_date
            """, (
                uid, local_data['username'], status, 
                sorted_dates[0], sorted_dates[-1], raw_data, int(time.time()*1000)
            ))
            
            if (i+1) % 10 == 0:
                print(f"   Fantasma {i+1}/{len(missing_ids)}: {uid} -> {status}")
                conn.commit()
            
            time.sleep(0.7) # Delay maior para requests individuais

        except Exception as e:
            print(f"   Erro checando {uid}: {e}")

    conn.commit()
    conn.close()
    print("✅ Histórico corrigido e banco atualizado com sucesso!")

# ================= EXECUÇÃO =================

if __name__ == "__main__":
    if not os.path.exists(DB_FILE):
        print("❌ Banco de dados não encontrado! Rode o init_db.py primeiro.")
    else:
        # 1. Ler arquivos locais
        users_map = scan_local_files()
        
        # 2. Atualizar DB
        if users_map:
            fetch_and_update_db(users_map)
        else:
            print("Nenhum dado encontrado nos arquivos.")