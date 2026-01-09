import sqlite3
import requests
import json
import time
import os

# ================= CONFIGURAÇÃO =================

DB_FILE = "team_users.db"
OUTPUT_DIR = "player_data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Lote de requisição (respeitando limites da API)
BATCH_SIZE = 300

HEADERS = {
    "User-Agent": "MegaStatusBot/4.0 (Kauan/TeamManager)",
    "Accept": "application/json"
}

# ================= FUNÇÕES DE EXTRAÇÃO =================

def extract_ratings_full(user_obj):
    """Extrai TODOS os ratings possíveis do objeto user"""
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
    """Extrai estatísticas de vitórias/derrotas e tempo jogado"""
    count = user_obj.get("count", {})
    return (
        count.get("all"),
        count.get("win"),
        count.get("loss"),
        count.get("draw"),
        user_obj.get("playTime", {}).get("total")
    )

def extract_profile(user_obj):
    """Extrai dados biográficos"""
    profile = user_obj.get("profile", {})
    return (
        profile.get("bio"),
        profile.get("country"),
        profile.get("location")
    )

# ================= API & DB =================

def bulk_fetch(ids):
    """Busca até 300 usuários de uma vez (ignora contas fechadas/missing)"""
    try:
        r = requests.post(
            "https://lichess.org/api/users",
            data=",".join(ids),
            headers=HEADERS,
            timeout=30
        )
        if r.status_code != 200:
            print(f"⚠️ Erro API Bulk ({r.status_code})...")
            return []
        return r.json()
    except Exception as e:
        print(f"⚠️ Exceção no bulk: {e}")
        return []

def fetch_individual_full(uid):
    """Busca usuário individualmente (para pegar banidos/fechados)"""
    try:
        r = requests.get(f"https://lichess.org/api/user/{uid}", headers=HEADERS, timeout=10)
        
        # 404 = Conta Deletada/Inexistente
        if r.status_code == 404:
            return "closed", None
        
        # Outros erros
        if r.status_code != 200:
            return None, None # Tenta de novo depois ou ignora
            
        data = r.json()
        
        # Determina status
        if data.get("disabled"):
            status = "closed"
        elif data.get("tosViolation"):
            status = "banned"
        else:
            status = "active" if data.get("seenAt") else "inactive"
            
        return status, data
        
    except Exception:
        return None, None

def update_user_db(cur, uid, data, status):
    """Atualiza o registro no banco com TODOS os campos novos"""
    
    ratings = extract_ratings_full(data)
    stats = extract_stats(data)
    profile = extract_profile(data)
    
    # Query Monstruosa para atualizar tudo
    cur.execute("""
        UPDATE users
        SET 
            username = ?,
            status = ?,
            bio = ?, country = ?, location = ?,
            
            rating_bullet = ?, rating_blitz = ?, rating_rapid = ?, rating_classical = ?, rating_correspondence = ?,
            rating_crazyhouse = ?, rating_chess960 = ?, rating_king_of_the_hill = ?, rating_three_check = ?,
            rating_antichess = ?, rating_atomic = ?, rating_horde = ?, rating_racing_kings = ?, rating_ultra_bullet = ?,
            rating_puzzle = ?,
            
            total_games = ?, total_wins = ?, total_losses = ?, total_draws = ?, play_time_total = ?,
            
            seen_at = ?,
            last_seen_api_timestamp = ?,
            raw_json = ?
            
        WHERE id_lichess = ?
    """, (
        data.get("username"), status,
        *profile,           # bio, country, location
        *ratings,           # 15 ratings
        *stats,             # 5 stats
        data.get("seenAt"), int(time.time()*1000), json.dumps(data),
        uid
    ))

# ================= UTIL =================

def chunk(lst, size):
    for i in range(0, len(lst), size):
        yield lst[i:i + size]

def export_json(conn, filename, query):
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    rows = cur.execute(query).fetchall()
    data = [dict(r) for r in rows]
    
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"   📄 {filename} gerado com {len(data)} registros.")

# ================= MAIN =================

def main():
    print("🔄 MEGA STATUS UPDATE v4.0 (Schema Completo)")
    
    if not os.path.exists(DB_FILE):
        print("❌ Banco de dados não encontrado! Rode o init_db.py primeiro.")
        return

    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    # 1. Carregar IDs
    cur.execute("SELECT id_lichess FROM users")
    ids = [r[0] for r in cur.fetchall()]
    ids = [uid.lower() for uid in ids if uid]
    print(f"👥 Total de usuários para verificar: {len(ids)}")

    appeared = set()

    # 2. BULK FETCH (Rápido)
    print("🚀 Iniciando atualização em massa...")
    for batch in chunk(ids, BATCH_SIZE):
        api_users = bulk_fetch(batch)
        
        for u in api_users:
            uid = u.get("id").lower()
            appeared.add(uid)
            
            # Status preliminar (será refinado se tiver flags)
            if u.get("disabled"): status = "closed"
            elif u.get("tosViolation"): status = "banned"
            else: status = "active" if u.get("seenAt") else "inactive"
            
            update_user_db(cur, uid, u, status)
            
        conn.commit()
        print(f"   Processados {len(appeared)} jogadores via Bulk...")
        time.sleep(1.0)

    # 3. SUSPEITOS (Lento)
    suspects = [uid for uid in ids if uid not in appeared]
    print(f"⚠️ {len(suspects)} usuários não retornaram no Bulk (Possíveis Banidos/Closed)...")
    
    count_updated = 0
    for i, uid in enumerate(suspects):
        status, data = fetch_individual_full(uid)
        
        if status == "closed" and data is None:
            # Conta deletada (404)
            cur.execute("UPDATE users SET status='closed', last_seen_api_timestamp=? WHERE id_lichess=?", (int(time.time()*1000), uid))
        elif data:
            # Conta existe (pode ser banida ou disabled)
            update_user_db(cur, uid, data, status)
        
        count_updated += 1
        if (i+1) % 10 == 0:
            print(f"   Investigando suspeitos: {i+1}/{len(suspects)}")
        
        time.sleep(0.7) # Delay
        
    conn.commit()
    print("✅ Banco de dados sincronizado!")

    # 4. EXPORTS
    print("📤 Gerando arquivos JSON atualizados...")
    
    # Dump completo
    export_json(conn, "users_full_dump.json", "SELECT * FROM users")
    
    # Exemplo: Ranking Rapid (apenas ativos)
    export_json(conn, "leaderboard_rapid.json", 
        """
        SELECT username, rating_rapid, total_games, country 
        FROM users 
        WHERE status='active' AND rating_rapid IS NOT NULL 
        ORDER BY rating_rapid DESC LIMIT 50
        """
    )
    
    # Exemplo: Banidos e Fechados
    export_json(conn, "bans_and_closures.json",
        "SELECT username, status, id_lichess FROM users WHERE status IN ('banned', 'closed')"
    )

    conn.close()

if __name__ == "__main__":
    main()