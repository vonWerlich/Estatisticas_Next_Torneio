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
    "User-Agent": "MonthlyStatusBot/2.3 (Kauan/TeamManager)",
    "Accept": "application/json"
}

# ================= API =================

def bulk_fetch(ids):
    try:
        r = requests.post(
            "https://lichess.org/api/users",
            data=",".join(ids),
            headers=HEADERS,
            timeout=20
        )
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"⚠️ Erro no bulk fetch: {e}")
        return []

def check_full_user(uid):
    """
    Consulta individual completa:
    - status
    - perfil
    - ratings
    """
    try:
        r = requests.get(
            f"https://lichess.org/api/user/{uid}",
            headers=HEADERS,
            timeout=10
        )

        if r.status_code == 404:
            return {"status": "closed"}

        if r.status_code == 429 or r.status_code >= 500:
            return None

        data = r.json()

        # Status
        if data.get("disabled"):
            status = "closed"
        elif data.get("tosViolation"):
            status = "banned"
        else:
            status = "active" if data.get("seenAt") else "inactive"

        result = {
            "status": status,
            "last_seen_api_timestamp": data.get("seenAt"),
            "real_name": data.get("profile", {}).get("realName"),
            "country": data.get("profile", {}).get("country"),
            "location": data.get("profile", {}).get("location"),
            "bio": data.get("profile", {}).get("bio"),
            "fide_rating": data.get("profile", {}).get("fideRating"),
            "ratings": {}
        }

        for perf, info in data.get("perfs", {}).items():
            rating = info.get("rating")
            if isinstance(rating, int):
                result["ratings"][perf] = rating

        return result

    except Exception:
        return None

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
    print("🔄 Atualização mensal de status e perfil")

    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    cur.execute("SELECT id_lichess FROM users")
    ids = [r[0].lower() for r in cur.fetchall() if r[0]]

    appeared = set()

    # ===== BULK =====
    for batch in chunk(ids, BATCH_SIZE):
        api_users = bulk_fetch(batch)

        for u in api_users:
            uid = u.get("id", "").lower()
            if not uid:
                continue

            appeared.add(uid)

            if u.get("disabled"):
                status = "closed"
            elif u.get("tosViolation"):
                status = "banned"
            else:
                status = "active" if u.get("seenAt") else "inactive"

            cur.execute("""
                UPDATE users
                SET status = ?,
                    last_seen_api_timestamp = ?
                WHERE id_lichess = ?
            """, (status, u.get("seenAt"), uid))

        conn.commit()
        time.sleep(1.0)

    # ===== INDIVIDUAL =====
    suspects = [uid for uid in ids if uid not in appeared]
    print(f"⚠️ Chamadas individuais: {len(suspects)}")

    PERF_MAP = {
        "bullet": "rating_bullet",
        "blitz": "rating_blitz",
        "rapid": "rating_rapid",
        "classical": "rating_classical",
        "ultraBullet": "rating_ultrabullet",
        "chess960": "rating_chess960",
        "crazyhouse": "rating_crazyhouse",
        "antichess": "rating_antichess",
        "atomic": "rating_atomic",
        "horde": "rating_horde",
        "racingKings": "rating_racing_kings",
        "threeCheck": "rating_three_check"
    }

    for i, uid in enumerate(suspects):
        data = check_full_user(uid)
        if data is None:
            continue

        updates = {
            "status": data["status"],
            "last_seen_api_timestamp": data.get("last_seen_api_timestamp"),
            "real_name": data.get("real_name"),
            "country": data.get("country"),
            "location": data.get("location"),
            "bio": data.get("bio"),
            "fide_rating": data.get("fide_rating")
        }

        for perf, rating in data.get("ratings", {}).items():
            col = PERF_MAP.get(perf)
            if col:
                updates[col] = rating

        set_clause = ", ".join(f"{k}=?" for k in updates)
        values = list(updates.values()) + [uid]

        cur.execute(
            f"UPDATE users SET {set_clause} WHERE id_lichess = ?",
            values
        )

        if (i + 1) % 10 == 0:
            print(f"  [{i+1}/{len(suspects)}] {uid}")

        time.sleep(0.7)

    conn.commit()

    # ===== EXPORTS =====
    export_json(conn, "users_all.json", "SELECT * FROM users")
    export_json(conn, "users_lurkers.json",
        """
        SELECT * FROM users
        WHERE first_seen_team_date IS NULL
          AND last_seen_team_date IS NULL
        """
    )
    export_json(conn, "users_banned.json", "SELECT * FROM users WHERE status = 'banned'")
    export_json(conn, "users_closed.json", "SELECT * FROM users WHERE status = 'closed'")
    export_json(conn, "members_active.json",
        """
        SELECT * FROM users
        WHERE is_team_member = 1 AND status = 'active'
        """
    )
    export_json(conn, "members_inactive.json",
        """
        SELECT * FROM users
        WHERE is_team_member = 1 AND status = 'inactive'
        """
    )

        # ===== EXPORTS torneios =====
    export_json(conn, "users_all.json", "SELECT * FROM users")

    export_json(conn, "users_lurkers.json",
        """
        SELECT * FROM users
        WHERE first_seen_team_date IS NULL
          AND last_seen_team_date IS NULL
        """
    )

    export_json(conn, "users_banned.json",
        "SELECT * FROM users WHERE status = 'banned'"
    )

    export_json(conn, "users_closed.json",
        "SELECT * FROM users WHERE status = 'closed'"
    )

    export_json(conn, "members_active.json",
        """
        SELECT * FROM users
        WHERE is_team_member = 1 AND status = 'active'
        """
    )

    export_json(conn, "members_inactive.json",
        """
        SELECT * FROM users
        WHERE is_team_member = 1 AND status = 'inactive'
        """
    )

    # ===== TORNEIOS =====
    export_json(conn, "tournaments_all.json",
        """
        SELECT *
        FROM tournaments
        ORDER BY tournament_start_datetime
        """
    )

    # ===== RESULTADOS (TODOS) =====
    export_json(conn, "tournament_results_all.json",
        """
        SELECT *
        FROM tournament_results
        ORDER BY tournament_id, final_rank
        """
    )

    # ===== RESULTADOS (TOP 3 POR TORNEIO) =====
    export_json(conn, "tournament_results_top3.json",
        """
        SELECT *
        FROM tournament_results
        WHERE final_rank <= 3
        ORDER BY tournament_id, final_rank
        """
    )

    # ===== RESULTADOS AGRUPADOS POR TORNEIO =====
    export_json(conn, "tournament_results_by_tournament.json",
        """
        SELECT
            t.tournament_id,
            t.tournament_name,
            t.tournament_start_datetime,
            r.user_id_lichess,
            r.final_rank,
            r.final_score,
            r.rating_at_start,
            r.performance_rating
        FROM tournaments t
        JOIN tournament_results r
          ON t.tournament_id = r.tournament_id
        ORDER BY t.tournament_start_datetime, r.final_rank
        """
    )


    conn.close()
    print("✅ Atualização concluída")

if __name__ == "__main__":
    main()
