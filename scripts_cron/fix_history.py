import os
import json
import sqlite3
import sys
from datetime import datetime, timezone

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

# --- CONFIG ---
DATA_DIR_TORNEIOS = "torneiosnew"
DATA_FOLDER = "data"
DB_FILE = os.path.join(DATA_FOLDER, "team_users.db")

DEFAULT_GHOST_CHECK_CUTOFF = "2020-05-08T18:30:00-03:00"

os.makedirs(DATA_DIR_TORNEIOS, exist_ok=True)
os.makedirs(DATA_FOLDER, exist_ok=True)

# --- UTIL ---
def carregar_json(path, default):
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return default

def converter_data_para_iso(starts_at):
    """
    Recebe string ISO do Lichess e normaliza para ISO UTC.
    """
    if not starts_at:
        return None
    try:
        dt = datetime.fromisoformat(starts_at.replace("Z", "+00:00"))
        return dt.astimezone(timezone.utc).isoformat()
    except:
        return None

def extrair_jogadores_dos_games(games_file):
    users = set()
    if not os.path.exists(games_file):
        return users

    with open(games_file, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            try:
                g = json.loads(line)
                w = g.get("players", {}).get("white", {}).get("user", {}).get("name")
                b = g.get("players", {}).get("black", {}).get("user", {}).get("name")
                if w:
                    users.add(w)
                if b:
                    users.add(b)
            except:
                pass
    return users

# --- MAIN ---
def run():
    print("🚀 Inicializando banco a partir do histórico")

    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    # --- ALTERAÇÃO AQUI: Criação das tabelas do zero ---
    cur.executescript("""
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
    );

    CREATE TABLE IF NOT EXISTS tournaments (
        tournament_id TEXT PRIMARY KEY,
        tournament_start_datetime TEXT,
        tournament_system TEXT,
        tournament_time_control TEXT,
        tournament_variant TEXT,
        tournament_rated INTEGER,
        number_of_players INTEGER,
        tournament_name TEXT,
        circuito TEXT -- <==== NOVO CAMPO ADICIONADO AQUI
    );

    CREATE TABLE IF NOT EXISTS tournament_results (
        tournament_id TEXT,
        user_id_lichess TEXT,
        final_rank INTEGER, final_score INTEGER, rating_at_start INTEGER, performance_rating INTEGER,
        PRIMARY KEY (tournament_id, user_id_lichess),
        FOREIGN KEY (tournament_id) REFERENCES tournaments(tournament_id),
        FOREIGN KEY (user_id_lichess) REFERENCES users(id_lichess)
    );
    """)
    conn.commit()
    # ---------------------------------------------------

    try:
        cutoff_dt = datetime.fromisoformat(
            DEFAULT_GHOST_CHECK_CUTOFF.replace("Z", "+00:00")
        )
    except:
        cutoff_dt = datetime.now(timezone.utc)

    files = [
        f.split("_")[0]
        for f in os.listdir(DATA_DIR_TORNEIOS)
        if f.endswith("_info.json")
    ]

    print(f"📂 Torneios encontrados: {len(files)}")

    for i, tid in enumerate(files):
        info = carregar_json(
            os.path.join(DATA_DIR_TORNEIOS, f"{tid}_info.json"), {}
        )
        results = carregar_json(
            os.path.join(DATA_DIR_TORNEIOS, f"{tid}_results.json"), []
        )

        # --- DATA DO TORNEIO ---
        t_iso = converter_data_para_iso(info.get("startsAt"))
        t_dt = None
        if t_iso:
            try:
                t_dt = datetime.fromisoformat(t_iso)
            except:
                pass


        # --- LÓGICA ESPELHADA DO UPDATE_TOURNAMENTS.PY ---
        final_name = info.get("fullName") or info.get("name") or "Torneio Sem Nome"
        final_system = info.get("system") or "swiss" # Se não tem o campo system, é swiss
        
        perf_key = info.get("perf", {}).get("key")
        if not perf_key and "clock" in info:
             limit = info.get("clock", {}).get("limit", 0)
             if limit < 180: perf_key = "bullet"
             elif limit < 480: perf_key = "blitz"
             elif limit < 1500: perf_key = "rapid"
             else: perf_key = "classical"

        # --- INSERE TORNEIO ---
        cur.execute("""
        INSERT OR IGNORE INTO tournaments (
            tournament_id,
            tournament_start_datetime,
            tournament_system,
            tournament_time_control,
            tournament_variant,
            tournament_rated,
            number_of_players,
            tournament_name
        )
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

        # --- USUÁRIOS DO RESULTADO ---
        users = set(r.get("username") for r in results if r.get("username"))

        # --- GHOST PLAYERS (GAMES) ---
        if t_dt and t_dt >= cutoff_dt:
            games_file = os.path.join(
                DATA_DIR_TORNEIOS, f"{tid}_games.ndjson"
            )
            users |= extrair_jogadores_dos_games(games_file)

        # --- UPSERT USERS ---
        for username in users:
            cur.execute("""
            INSERT INTO users (
                id_lichess,
                status,
                is_team_member,
                first_seen_team_date,
                last_seen_team_date,
                created_at
            )
            VALUES (?, 'inactive', 1, ?, ?, strftime('%s','now'))
            ON CONFLICT(id_lichess) DO UPDATE SET
                first_seen_team_date =
                    CASE
                        WHEN users.first_seen_team_date IS NULL
                             OR users.first_seen_team_date > excluded.first_seen_team_date
                        THEN excluded.first_seen_team_date
                        ELSE users.first_seen_team_date
                    END,
                last_seen_team_date =
                    CASE
                        WHEN users.last_seen_team_date IS NULL
                             OR users.last_seen_team_date < excluded.last_seen_team_date
                        THEN excluded.last_seen_team_date
                        ELSE users.last_seen_team_date
                    END
            """, (username, t_iso, t_iso))

        # --- RESULTADOS DO TORNEIO ---
        for r in results:
            username = r.get("username")
            if not username:
                continue

            cur.execute("""
            INSERT OR IGNORE INTO tournament_results (
                tournament_id,
                user_id_lichess,
                final_rank,
                final_score,
                rating_at_start,
                performance_rating
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """, (
                tid,
                username,
                r.get("rank"),
                r.get("score"),
                r.get("rating"),
                r.get("performance")
            ))

        if (i + 1) % 10 == 0:
            print(f"  ... {i+1}/{len(files)} torneios processados")

    conn.commit()
    conn.close()
    print("✅ Banco inicializado com sucesso")

if __name__ == "__main__":
    run()
