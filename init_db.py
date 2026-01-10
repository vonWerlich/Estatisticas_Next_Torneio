import sqlite3
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

conn = sqlite3.connect("team_users.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    -- Identidade
    id_lichess TEXT PRIMARY KEY,

    -- Status Lichess
    status TEXT NOT NULL CHECK (
        status IN ('active', 'inactive', 'banned', 'closed')
    ),

    -- Vínculo com o time
    is_team_member INTEGER NOT NULL CHECK (is_team_member IN (0,1)),

    -- Datas baseadas em torneios (NÃO REMOVER)
    first_seen_team_date TEXT,
    last_seen_team_date TEXT,

    -- Última vez visto pela API
    last_seen_api_timestamp INTEGER,

    -- Perfil público
    real_name TEXT,
    country TEXT,
    location TEXT,
    bio TEXT,
    fide_rating INTEGER,

    -- Ratings Lichess (todos INTEGER, NULL se desconhecido)
    rating_bullet INTEGER,
    rating_blitz INTEGER,
    rating_rapid INTEGER,
    rating_classical INTEGER,
    rating_ultrabullet INTEGER,

    rating_chess960 INTEGER,
    rating_crazyhouse INTEGER,
    rating_antichess INTEGER,
    rating_atomic INTEGER,
    rating_horde INTEGER,
    rating_racing_kings INTEGER,
    rating_three_check INTEGER,

    -- Controle
    created_at INTEGER
)
""")

conn.commit()
conn.close()

print("✅ Banco inicializado")
