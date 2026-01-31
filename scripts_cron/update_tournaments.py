import os
import sqlite3
import requests
import json
import time
import sys
from datetime import datetime, timezone

# --- CONFIGURAÇÃO ---
DATA_FOLDER = "data"
DB_FILE = os.path.join(DATA_FOLDER, "team_users.db")
TEAM_ID = "next-nucleo-de-estudos-em-xadrez--tecnologias"
DATA_DIR_TORNEIOS = os.path.join(DATA_FOLDER, "raw_tournaments")

BATCH_SIZE = 100         # Lote por requisição (Segurança API)
PROFILE_UPDATE_LIMIT = 2000  # Quantos perfis atualizar por execução

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

os.makedirs(DATA_FOLDER, exist_ok=True)
os.makedirs(DATA_DIR_TORNEIOS, exist_ok=True)

# ==============================================================================
# 1. GERENCIAMENTO DE BANCO DE DADOS
# ==============================================================================
def ensure_database():
    print("🛠️ Verificando integridade do banco de dados...")
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id_lichess TEXT PRIMARY KEY,
        status TEXT DEFAULT 'active',
        is_team_member INTEGER DEFAULT 0,
        first_seen_team_date TEXT,
        last_seen_team_date TEXT,
        last_seen_api_timestamp INTEGER,
        last_updated_at INTEGER,
        real_name TEXT, country TEXT, location TEXT, bio TEXT, fide_rating INTEGER,
        rating_bullet INTEGER, rating_blitz INTEGER, rating_rapid INTEGER, rating_classical INTEGER,
        rating_ultrabullet INTEGER, rating_chess960 INTEGER, rating_crazyhouse INTEGER,
        rating_antichess INTEGER, rating_atomic INTEGER, rating_horde INTEGER,
        rating_racing_kings INTEGER, rating_three_check INTEGER,
        created_at INTEGER
    )""")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS tournaments (
        tournament_id TEXT PRIMARY KEY,
        tournament_start_datetime TEXT,
        tournament_system TEXT,
        tournament_time_control TEXT,
        tournament_variant TEXT,
        tournament_rated INTEGER,
        number_of_players INTEGER,
        tournament_name TEXT
    )""")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS tournament_results (
        tournament_id TEXT,
        user_id_lichess TEXT,
        final_rank INTEGER, final_score INTEGER, rating_at_start INTEGER, performance_rating INTEGER,
        PRIMARY KEY (tournament_id, user_id_lichess),
        FOREIGN KEY (tournament_id) REFERENCES tournaments(tournament_id),
        FOREIGN KEY (user_id_lichess) REFERENCES users(id_lichess)
    )""")
    
    conn.commit()
    conn.close()

# ==============================================================================
# 2. TORNEIOS (CORRIGIDO: SWISS vs ARENA)
# ==============================================================================
def converter_data_iso(starts_at):
    if not starts_at: return None
    try:
        dt = datetime.fromisoformat(starts_at.replace("Z", "+00:00"))
        return dt.astimezone(timezone.utc).isoformat()
    except: return None

def process_tournament_sql(tid, info, results, games_path, conn, manual_system_type):
    cur = conn.cursor()
    
    t_iso = converter_data_iso(info.get("startsAt"))
    
    # --- CORREÇÃO DE NOME E SISTEMA ---
    # Arena usa 'fullName', Swiss usa 'name'
    # Arena usa 'system', Swiss as vezes não tem -> usamos o manual_system_type
    
    final_name = info.get("fullName") or info.get("name") or "Torneio Sem Nome"
    final_system = info.get("system") or manual_system_type
    
    # Info de ritmo
    # Arena: perf.key ou timeControl... Swiss: clock...
    # Vamos tentar pegar o mais generico possivel ou deixar NULL se falhar
    perf_key = info.get("perf", {}).get("key")
    if not perf_key and "clock" in info:
         # Tenta deduzir ritmo do swiss se nao tiver perf (ex: limit/60 = min)
         limit = info.get("clock", {}).get("limit", 0)
         if limit < 180: perf_key = "bullet"
         elif limit < 480: perf_key = "blitz"
         elif limit < 1500: perf_key = "rapid"
         else: perf_key = "classical"

    cur.execute("""
    INSERT OR IGNORE INTO tournaments 
    (tournament_id, tournament_start_datetime, tournament_system, tournament_time_control, 
     tournament_variant, tournament_rated, number_of_players, tournament_name)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        tid, 
        t_iso, 
        final_system, 
        perf_key,
        info.get("variant"), 
        1 if info.get("rated") else 0, 
        info.get("nbPlayers"), 
        final_name
    ))

    # Identificar jogadores (Results + Games Files)
    players_found = set(r.get("username").lower() for r in results if r.get("username"))
    
    if os.path.exists(games_path):
        try:
            with open(games_path, "r", encoding="utf-8") as f:
                for line in f:
                    if not line.strip(): continue
                    g = json.loads(line)
                    w = g.get("players", {}).get("white", {}).get("user", {}).get("name")
                    b = g.get("players", {}).get("black", {}).get("user", {}).get("name")
                    if w: players_found.add(w.lower())
                    if b: players_found.add(b.lower())
        except Exception: pass

    # Upsert Users (Garante que existem na tabela users)
    for username in players_found:
        cur.execute("""
        INSERT INTO users (id_lichess, created_at) VALUES (?, strftime('%s','now'))
        ON CONFLICT(id_lichess) DO UPDATE SET
            first_seen_team_date = CASE WHEN first_seen_team_date IS NULL OR first_seen_team_date > ? THEN ? ELSE first_seen_team_date END,
            last_seen_team_date = CASE WHEN last_seen_team_date IS NULL OR last_seen_team_date < ? THEN ? ELSE last_seen_team_date END
        """, (username, t_iso, t_iso, t_iso, t_iso))

    # Inserir Resultados
    for r in results:
        uname = r.get("username", "").lower()
        if not uname: continue
        cur.execute("""
        INSERT OR IGNORE INTO tournament_results (tournament_id, user_id_lichess, final_rank, final_score, rating_at_start, performance_rating)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (tid, uname, r.get("rank"), r.get("score"), r.get("rating"), r.get("performance")))
    
    conn.commit()

def sync_tournaments():
    print("\n🏆 Sincronizando Torneios...")
    conn = sqlite3.connect(DB_FILE)
    existing_ids_db = set(row[0] for row in conn.execute("SELECT tournament_id FROM tournaments"))
    
    # --- CORREÇÃO: ARENA vs SWISS ---
    urls = [(f"https://lichess.org/api/team/{TEAM_ID}/arena", "arena"),
            (f"https://lichess.org/api/team/{TEAM_ID}/swiss", "swiss")]
    
    tournaments_to_process = []
    print("   -> Buscando lista na API...")
    
    for url, tipo_manual in urls:
        try:
            resp = requests.get(url)
            if resp.status_code == 200:
                for line in resp.iter_lines():
                    if line:
                        d = json.loads(line)
                        if d["id"] not in existing_ids_db:
                            # AQUI ESTÁ O PULO DO GATO: Salvamos o tipo manual no objeto
                            d["type_manual"] = tipo_manual 
                            tournaments_to_process.append(d)
        except Exception as e: print(f"   ⚠️ Erro ao listar {tipo_manual}: {e}")

    print(f"   -> {len(tournaments_to_process)} novos torneios para processar.")

    for t in tournaments_to_process:
        tid = t["id"]
        # Recupera o tipo correto que salvamos lá em cima
        sys_type = t.get("type_manual", "arena") 
        
        file_info = os.path.join(DATA_DIR_TORNEIOS, f"{tid}_info.json")
        file_results = os.path.join(DATA_DIR_TORNEIOS, f"{tid}_results.json")
        file_games = os.path.join(DATA_DIR_TORNEIOS, f"{tid}_games.ndjson")
        
        # Define a URL base correta baseado no tipo
        if sys_type == "swiss":
            base_url = f"https://lichess.org/api/swiss/{tid}"
        else:
            base_url = f"https://lichess.org/api/tournament/{tid}"

        need_download = not (os.path.exists(file_info) and os.path.exists(file_results))
        
        if need_download:
            print(f"   📥 Baixando {sys_type.upper()} {tid} ({t.get('fullName') or t.get('name')})...")
            try:
                # 1. Info
                info = requests.get(base_url).json()
                with open(file_info, "w", encoding="utf-8") as f: json.dump(info, f)

                # 2. Results
                res_txt = requests.get(f"{base_url}/results", headers={"Accept": "application/x-ndjson"}).text
                results = [json.loads(l) for l in res_txt.strip().split('\n') if l]
                with open(file_results, "w", encoding="utf-8") as f: json.dump(results, f)

                # 3. Games
                with requests.get(f"{base_url}/games", stream=True, headers={"Accept": "application/x-ndjson"}) as r, open(file_games, "w", encoding="utf-8") as f:
                    for line in r.iter_lines(): 
                        if line: f.write(line.decode('utf-8') + '\n')
            except Exception as e:
                print(f"❌ Erro download {tid}: {e}")
                continue
        else:
            print(f"   📂 Lendo local {tid}...")

        try:
            with open(file_info, "r", encoding="utf-8") as f: info = json.load(f)
            with open(file_results, "r", encoding="utf-8") as f: results = json.load(f)
            # Passamos o sys_type para garantir que grave 'swiss' ou 'arena' no banco
            process_tournament_sql(tid, info, results, file_games, conn, sys_type)
        except Exception as e:
            print(f"❌ Erro JSON {tid}: {e}")

    conn.close()

# ==============================================================================
# 3. MEMBROS (SYNC)
# ==============================================================================
def sync_members_status():
    print("\n👥 Sincronizando lista de membros...")
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    
    cur.execute("UPDATE users SET is_team_member = 0")
    
    current_ids = []
    try:
        with requests.get(f"https://lichess.org/api/team/{TEAM_ID}/users", stream=True) as r:
            for line in r.iter_lines():
                if line:
                    u = json.loads(line)
                    current_ids.append((u["id"],))
    except Exception as e:
        print(f"   ❌ Erro API membros: {e}")
        return

    cur.executemany("""
    INSERT INTO users (id_lichess, is_team_member, created_at, status) 
    VALUES (?, 1, strftime('%s','now'), 'active')
    ON CONFLICT(id_lichess) DO UPDATE SET is_team_member = 1
    """, current_ids)
    
    conn.commit()
    conn.close()

# ==============================================================================
# 4. ATUALIZAÇÃO DE PERFIS (COM DETECÇÃO DE BANIDOS)
# ==============================================================================
def update_profiles_data():
    print("\n🕵️ Atualizando perfis (Fila Inteligente)...")
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    # Pega quem nunca foi atualizado ou os mais antigos
    cur.execute("""
        SELECT id_lichess 
        FROM users 
        ORDER BY 
            CASE WHEN last_updated_at IS NULL THEN 0 ELSE 1 END ASC,
            is_team_member DESC,
            last_updated_at ASC
        LIMIT ?
    """, (PROFILE_UPDATE_LIMIT,))
    
    rows = cur.fetchall()
    ids_to_update = [r[0] for r in rows]
    total = len(ids_to_update)

    print(f"   -> Processando {total} usuários...")

    for i in range(0, total, BATCH_SIZE):
        chunk = ids_to_update[i : i + BATCH_SIZE]
        now_ts = int(time.time())

        sys.stdout.write(f"\r      ⏳ Lote {i//BATCH_SIZE + 1}...")
        sys.stdout.flush()

        try:
            resp = requests.post("https://lichess.org/api/users", data=",".join(chunk))
            if resp.status_code == 200:
                users_data = resp.json()
                update_list = []
                
                for u in users_data:
                    prof = u.get("profile", {})
                    perfs = u.get("perfs", {})
                    
                    # --- AQUI ESTÁ A CORREÇÃO DA LÓGICA DE STATUS ---
                    status_api = 'active'
                    if u.get('tosViolation'):        # <--- O Lichess marca trapaceiros assim
                        status_api = 'banned'
                    elif u.get('closed') or u.get('disabled'):
                        status_api = 'closed'
                    # -----------------------------------------------
                    
                    update_list.append((
                        status_api,   # Agora passa 'banned', 'closed' ou 'active'
                        prof.get("firstName") or prof.get("lastName"), 
                        prof.get("country"), 
                        prof.get("location"), 
                        prof.get("bio"), 
                        prof.get("fideRating"),
                        perfs.get("bullet", {}).get("rating"), 
                        perfs.get("blitz", {}).get("rating"),
                        perfs.get("rapid", {}).get("rating"), 
                        perfs.get("classical", {}).get("rating"),
                        perfs.get("ultraBullet", {}).get("rating"), 
                        perfs.get("chess960", {}).get("rating"), 
                        perfs.get("crazyhouse", {}).get("rating"), 
                        perfs.get("antichess", {}).get("rating"), 
                        perfs.get("atomic", {}).get("rating"), 
                        perfs.get("horde", {}).get("rating"), 
                        perfs.get("racingKings", {}).get("rating"), 
                        perfs.get("threeCheck", {}).get("rating"), 
                        u.get("seenAt"),
                        now_ts,
                        u.get("id")
                    ))

                cur.executemany("""
                UPDATE users SET 
                    status = ?, real_name = ?, country = ?, location = ?, bio = ?, fide_rating = ?,
                    rating_bullet = ?, rating_blitz = ?, rating_rapid = ?, rating_classical = ?,
                    rating_ultrabullet = ?, rating_chess960 = ?, rating_crazyhouse = ?, 
                    rating_antichess = ?, rating_atomic = ?, rating_horde = ?, 
                    rating_racing_kings = ?, rating_three_check = ?,
                    last_seen_api_timestamp = ?,
                    last_updated_at = ?
                WHERE id_lichess = ?
                """, update_list)
                conn.commit()
            time.sleep(0.6)
        except Exception as e: 
            print(f"\n❌ Erro chunk: {e}")

    print(f"\n   ✅ Concluído.")
    conn.close()

# ==============================================================================
# MAIN
# ==============================================================================
def main():
    print("🚀 INICIANDO UPDATE (CORREÇÃO SWISS/ARENA)")
    ensure_database()
    sync_tournaments()
    sync_members_status()
    update_profiles_data()
    print("\n✅ FIM.")

if __name__ == "__main__":
    main()