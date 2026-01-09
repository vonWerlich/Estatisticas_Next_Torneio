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
    "User-Agent": "MonthlyStatusBot/2.2 (Kauan/TeamManager)",
    "Accept": "application/json"
}

# ================= API =================

def bulk_fetch(ids):
    """
    Busca usuários em lote (até 300 por vez).
    O Lichess SILENCIOSAMENTE remove usuários fechados/inexistentes desta resposta.
    """
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

def check_full_status_individual(uid):
    """
    Verifica individualmente e retorna o status exato e a flag de fechada.
    Retorna tupla: (status, is_closed) ou (None, None) em caso de erro de rede.
    """
    try:
        r = requests.get(
            f"https://lichess.org/api/user/{uid}",
            headers=HEADERS,
            timeout=10
        )

        # 404 = Conta não existe mais (Deletada definitivamente ou nunca existiu)
        if r.status_code == 404:
            return "closed", 1

        # Se for erro de servidor ou rate limit, não assuma nada
        if r.status_code == 429 or r.status_code >= 500:
            print(f"⚠️ Rate limit ou erro no Lichess para {uid} (Code {r.status_code}). Pulando...")
            return None, None

        data = r.json()

        # 1. Checagem de conta fechada (User closed)
        # A API retorna o objeto, mas com "disabled": true
        if data.get("disabled", False) is True:
            return "closed", 1
        
        # 2. Checagem de banimento (Lichess banned)
        if data.get("tosViolation", False) is True:
            return "banned", 0 # Banido geralmente não é conta fechada, é conta ativa mas restrita

        # 3. Ativo ou Inativo (baseado no ultimo login)
        if data.get("seenAt"):
            return "active", 0
        else:
            return "inactive", 0

    except Exception as e:
        # Se der erro de parsing ou conexão, retorna None para preservar o estado atual
        return None, None

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
    print("🔄 Atualização mensal de status (Versão Corrigida v2.2)")

    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    # ===== TODOS OS IDS =====
    cur.execute("SELECT id_lichess FROM users")
    ids = [r[0] for r in cur.fetchall()]
    # Normalizar para minúsculo para evitar duplicatas de case
    ids = [uid.lower() for uid in ids if uid]

    print(f"👥 Usuários no banco para verificar: {len(ids)}")

    appeared = set()

    # ===== 1. BULK CHECK (Rápido) =====
    print("🚀 Iniciando verificação em massa...")
    for batch in chunk(ids, BATCH_SIZE):
        api_users = bulk_fetch(batch)

        for u in api_users:
            uid = u.get("id")
            if not uid:
                continue

            uid = uid.lower()
            appeared.add(uid)

            # Prioridade de Status no Bulk
            if u.get("disabled", False):
                status = "closed"
                closed_acc = 1
            elif u.get("tosViolation", False):
                status = "banned"
                closed_acc = 0
            else:
                status = "active" if u.get("seenAt") else "inactive"
                closed_acc = 0

            cur.execute("""
                UPDATE users
                SET status = ?,
                    closed_account = ?,
                    last_seen_api_timestamp = ?
                WHERE id_lichess = ?
            """, (status, closed_acc, u.get("seenAt"), uid))

        conn.commit()
        time.sleep(1.0) # Respeitando a API

    # ===== 2. SUSPEITOS (Lento e Preciso) =====
    # Quem estava na lista de IDs mas NÃO veio no bulk é suspeito de estar fechado/missing
    suspects = [uid for uid in ids if uid not in appeared]
    print(f"⚠️ Suspeitos de conta fechada (não retornados no bulk): {len(suspects)}")

    count_closed = 0
    count_errors = 0

    for i, uid in enumerate(suspects):
        real_status, is_closed = check_full_status_individual(uid)

        # Se deu erro de conexão (None), ignoramos este user nesta rodada
        if real_status is None:
            count_errors += 1
            continue

        # Log visual a cada 10 users
        if (i + 1) % 10 == 0:
            print(f"  [{i+1}/{len(suspects)}] Verificando {uid} -> {real_status}")

        cur.execute("""
            UPDATE users
            SET status = ?,
                closed_account = ?
            WHERE id_lichess = ?
        """, (real_status, is_closed, uid))
        
        if real_status == "closed":
            count_closed += 1

        # Delay maior aqui pois são requisições individuais
        time.sleep(0.7) 

    conn.commit()
    print(f"✅ Suspeitos processados. {count_closed} confirmados como fechados. {count_errors} erros de conexão.")

    # ================= EXPORTS =================

    print("📤 Exportando JSONs atualizados...")

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
        WHERE is_team_member = 1
          AND status = 'active'
          AND closed_account = 0
        """
    )

    export_json(conn, "members_inactive.json",
        """
        SELECT * FROM users
        WHERE is_team_member = 1
          AND status = 'inactive'
          AND closed_account = 0
        """
    )

    conn.close()
    print("✅ Atualização mensal concluída com sucesso!")

if __name__ == "__main__":
    main()