import sqlite3
import requests
import json
import time
import os

# ================= CONFIG =================

DB_FILE = "team_users.db"
OUTPUT_DIR = "player_data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

BATCH_SIZE = 300

HEADERS = {
    "User-Agent": "MonthlyStatusBot/2.0",
    "Accept": "application/json"
}

# ================= API =================

def bulk_fetch(ids):
    r = requests.post(
        "https://lichess.org/api/users",
        data=",".join(ids),
        headers=HEADERS,
        timeout=20
    )
    r.raise_for_status()
    return r.json()

def check_closed_individual(uid):
    try:
        r = requests.get(
            f"https://lichess.org/api/user/{uid}",
            headers=HEADERS,
            timeout=10
        )
        if r.status_code == 404:
            return True
        if r.status_code == 200:
            return False
        return False
    except Exception:
        return False

# ================= UTIL =================

def chunk(lst, size):
    for i in range(0, len(lst), size):
        yield lst[i:i + size]

def export_json(conn, filename, query):
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    rows = cur.execute(query).fetchall()
    data = [dict(r) for r in rows]

    with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ================= MAIN =================

def main():
    print("🔄 Atualização mensal de status iniciada")

    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    # ===== TODOS OS IDS =====
    cur.execute("SELECT id_lichess FROM users")
    ids = [r[0] for r in cur.fetchall()]

    print(f"👥 Usuários no banco: {len(ids)}")

    appeared = set()

    # ===== BULK =====
    for batch in chunk(ids, BATCH_SIZE):
        api_users = bulk_fetch(batch)

        for u in api_users:
            uid = u.get("id")
            if not uid:
                continue

            uid = uid.lower()
            appeared.add(uid)

            if u.get("tosViolation"):
                status = "banned"
            else:
                status = "active" if u.get("seenAt") else "inactive"

            cur.execute("""
                UPDATE users
                SET status = ?,
                    closed_account = 0,
                    last_seen_api_timestamp = ?
                WHERE id_lichess = ?
            """, (status, u.get("seenAt"), uid))

        conn.commit()
        time.sleep(1.5)

    # ===== SUSPEITOS (NÃO APARECERAM NO BULK) =====
    suspects = [uid for uid in ids if uid not in appeared]
    print(f"⚠️ Suspeitos de conta fechada: {len(suspects)}")

    for uid in suspects:
        closed = check_closed_individual(uid)

        cur.execute("""
            UPDATE users
            SET closed_account = ?,
                status = CASE WHEN ? THEN 'closed' ELSE status END
            WHERE id_lichess = ?
        """, (1 if closed else 0, closed, uid))

        time.sleep(0.25)

    conn.commit()

    # ================= EXPORTS =================

    print("📤 Exportando JSONs")

    export_json(conn, "users_all.json", "SELECT * FROM users")

    export_json(conn, "users_lurkers.json", """
        SELECT * FROM users
        WHERE first_seen_team_date IS NULL
          AND last_seen_team_date IS NULL
    """)

    export_json(conn, "users_banned.json", """
        SELECT * FROM users
        WHERE status = 'banned'
    """)

    export_json(conn, "members_active.json", """
        SELECT * FROM users
        WHERE is_team_member = 1
          AND status = 'active'
          AND closed_account = 0
    """)

    export_json(conn, "members_inactive.json", """
        SELECT * FROM users
        WHERE is_team_member = 1
          AND status = 'inactive'
          AND closed_account = 0
    """)

    conn.close()
    print("✅ Atualização mensal concluída com sucesso")

if __name__ == "__main__":
    main()
