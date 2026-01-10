import os
import json
import sqlite3
from datetime import datetime, timezone

# --- CONFIG ---
DATA_DIR_TORNEIOS = "torneiosnew"
DB_FILE = "team_users.db"

DEFAULT_GHOST_CHECK_CUTOFF = "2020-05-08T18:30:00-03:00"

os.makedirs(DATA_DIR_TORNEIOS, exist_ok=True)

# --- UTIL ---
def carregar_json(path, default):
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return default

def converter_data_para_iso(ms):
    if ms is None:
        return None
    try:
        return datetime.fromtimestamp(ms / 1000, tz=timezone.utc).isoformat()
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
        info = carregar_json(os.path.join(DATA_DIR_TORNEIOS, f"{tid}_info.json"), {})
        results = carregar_json(os.path.join(DATA_DIR_TORNEIOS, f"{tid}_results.json"), [])

        t_iso = converter_data_para_iso(info.get("startsAt"))
        t_dt = None
        if t_iso:
            try:
                t_dt = datetime.fromisoformat(t_iso.replace("Z", "+00:00"))
            except:
                pass

        users = set(r.get("username") for r in results if r.get("username"))

        if t_dt and t_dt >= cutoff_dt:
            games = os.path.join(DATA_DIR_TORNEIOS, f"{tid}_games.ndjson")
            users |= extrair_jogadores_dos_games(games)

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

        if (i + 1) % 10 == 0:
            print(f"  ... {i+1}/{len(files)} torneios processados")

    conn.commit()
    conn.close()
    print("✅ Banco inicializado com sucesso")

if __name__ == "__main__":
    run()
