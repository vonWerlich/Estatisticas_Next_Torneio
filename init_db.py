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
    id_lichess TEXT PRIMARY KEY,
    status TEXT NOT NULL CHECK (
        status IN ('active', 'inactive', 'banned', 'closed')
    ),
    closed_account INTEGER NOT NULL CHECK (closed_account IN (0,1)),
    is_team_member INTEGER NOT NULL CHECK (is_team_member IN (0,1)),
    first_seen_team_date TEXT,
    last_seen_team_date TEXT,
    last_seen_api_timestamp INTEGER,
    created_at INTEGER
)
""")

conn.commit()
conn.close()

print("✅ Banco inicializado")
