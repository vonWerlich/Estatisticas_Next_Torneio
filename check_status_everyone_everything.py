import requests
import json
import os
import sys
import time
from datetime import datetime, timedelta, timezone

# ================= CONFIG =================

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

DATA_DIR = "player_data"
os.makedirs(DATA_DIR, exist_ok=True)

FILES = {
    "players": os.path.join(DATA_DIR, "players.json"),
    "lurkers": os.path.join(DATA_DIR, "lurkers.json"),
    "ex_members": os.path.join(DATA_DIR, "ex_members.json"),
}

BATCH_SIZE = 300
TEAM_INACTIVITY_DAYS = 547

HEADERS = {
    "User-Agent": "StatusChecker/1.2 (hybrid-fixed)",
    "Accept": "application/json"
}

# ================= UTIL =================

def load_json(path):
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def chunk(lst, size):
    for i in range(0, len(lst), size):
        yield lst[i:i + size]

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

        return False  # fallback conservador
    except Exception:
        return False

# ================= STATUS =================

def update_status_from_bulk(api_users, master):
    seen = set()

    for u in api_users:
        uid = u.get("id")
        if not uid:
            continue

        uid = uid.lower()
        seen.add(uid)

        entry = master.get(uid)
        if not entry:
            continue

        # Conta existe
        for ref in entry["refs"]:
            ref["closed_account"] = False

            if u.get("tosViolation"):
                ref["status"] = "banned"
            else:
                ref.setdefault("status", "inactive")

            ref["last_seen_api_timestamp"] = u.get("seenAt")

    return seen

def update_inactivity(players):
    now = datetime.now(timezone.utc)
    limit = timedelta(days=TEAM_INACTIVITY_DAYS)

    for p in players:
        if p.get("status") == "banned":
            continue
        if p.get("closed_account"):
            continue

        last = p.get("last_seen_team_date")
        if not last:
            continue

        try:
            dt = datetime.fromisoformat(last.replace("Z", "+00:00"))
            p["status"] = "inactive" if (now - dt) > limit else "active"
        except Exception:
            pass

# ================= MAIN =================

def main():
    players = load_json(FILES["players"])
    lurkers = load_json(FILES["lurkers"])
    ex_members = load_json(FILES["ex_members"])

    all_lists = players + lurkers + ex_members

    # master[uid] = { "refs": [obj1, obj2, ...] }
    master = {}
    ids = []

    # ===== NORMALIZAÇÃO =====

    for p in all_lists:
        uid = (p.get("id_lichess") or p.get("username") or "").lower()
        if not uid:
            continue

        p["id_lichess"] = uid
        p["closed_account"] = None
        p.setdefault("status", "inactive")
        p.setdefault("last_seen_api_timestamp", None)

        if uid not in master:
            master[uid] = {"refs": []}
            ids.append(uid)

        master[uid]["refs"].append(p)

    ids = list(set(ids))

    print(f"🔍 Usuários únicos: {len(ids)}")

    # ===== BULK =====

    appeared = set()

    for batch in chunk(ids, BATCH_SIZE):
        api_users = bulk_fetch(batch)
        seen = update_status_from_bulk(api_users, master)
        appeared |= seen
        time.sleep(1.5)

    # ===== SUSPEITOS =====

    suspects = [
        uid for uid, entry in master.items()
        if all(ref["closed_account"] is None for ref in entry["refs"])
    ]

    print(f"⚠️ Suspeitos de conta fechada: {len(suspects)}")

    # ===== INDIVIDUAL =====

    for uid in suspects:
        closed = check_closed_individual(uid)
        for ref in master[uid]["refs"]:
            ref["closed_account"] = closed
        time.sleep(0.25)

    # ===== GARANTIA FINAL (SEM NULL) =====

    for entry in master.values():
        for ref in entry["refs"]:
            if ref["closed_account"] is None:
                ref["closed_account"] = False

    # ===== STATUS LOCAL =====

    update_inactivity(players)

    # ===== SAVE =====

    save_json(FILES["players"], players)
    save_json(FILES["lurkers"], lurkers)
    save_json(FILES["ex_members"], ex_members)

    print("✅ Verificação híbrida concluída sem NULLs")

if __name__ == "__main__":
    main()
