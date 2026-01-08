import requests
import json
import os
import sys
import time
from datetime import datetime, timedelta, timezone

# --- CONFIGURAÇÃO ---
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

DATA_DIR_PLAYERS = "player_data"

FILES_CONFIG = {
    "players": os.path.join(DATA_DIR_PLAYERS, "players.json"),
    "lurkers": os.path.join(DATA_DIR_PLAYERS, "lurkers.json"),
    "ex_members": os.path.join(DATA_DIR_PLAYERS, "ex_members.json")
}

BANNED_FILE = os.path.join(DATA_DIR_PLAYERS, "banned_players.json")
INACTIVE_FILE = os.path.join(DATA_DIR_PLAYERS, "inactive_players.json")
METADATA_FILE = os.path.join(DATA_DIR_PLAYERS, "status_metadata.json")

TEAM_INACTIVITY_DAYS = 547
BATCH_SIZE = 300 

def carregar_json(filepath):
    if not os.path.exists(filepath): return []
    try:
        with open(filepath, "r", encoding="utf-8") as f: return json.load(f)
    except: return []

def salvar_json(filepath, data):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def chunk_list(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def processar_lote_invertido(api_users, master_map, requested_batch_ids):
    """
    Lógica Simplificada (Sugestão do Usuário):
    1. Marca TODOS do lote como 'closed_account = True'.
    2. Quem a API retornar, atualizamos e marcamos como 'False' (se não estiver disabled).
    """
    count_updated = 0
    
    # --- PASSO 1: O MASSACRE (Marca todo mundo do lote como fechado preventivamente) ---
    for req_id in requested_batch_ids:
        local_obj = master_map.get(req_id)
        if local_obj:
            local_obj["closed_account"] = True 
            # Se a API não devolver esse cara, ele já fica como True. Fim.

    # --- PASSO 2: A RESSURREIÇÃO (Quem a API devolveu, a gente "abre" a conta) ---
    for api_data in api_users:
        uid = api_data.get("id")
        local_obj = master_map.get(uid)
        
        if local_obj:
            count_updated += 1
            
            # Checa se a API diz explicitamente que está fechada
            esta_desativada = api_data.get("disabled", False)
            
            # Se NÃO estiver desativada na API, ressuscitamos (False)
            # Se estiver desativada, mantemos o True que definimos no Passo 1
            if not esta_desativada:
                local_obj["closed_account"] = False

            # --- Atualização de Dados (Igual antes) ---
            local_obj["username"] = api_data.get("username", local_obj.get("username"))
            local_obj["title"] = api_data.get("title")
            local_obj["country"] = api_data.get("profile", {}).get("country")
            
            # Status Banido
            if api_data.get("tosViolation"):
                local_obj["status"] = "banned"
            else:
                if local_obj.get("status") == "banned":
                    local_obj["status"] = "active"
                
            local_obj["last_seen_api_timestamp"] = api_data.get("seenAt")
            local_obj["created_at"] = api_data.get("createdAt")
            
            perfs = api_data.get("perfs", {})
            local_obj["rating_blitz"] = perfs.get("blitz", {}).get("rating")
            local_obj["rating_rapid"] = perfs.get("rapid", {}).get("rating")
            local_obj["rating_bullet"] = perfs.get("bullet", {}).get("rating")
            local_obj["rating_puzzle"] = perfs.get("puzzle", {}).get("rating")
            
            cnt = api_data.get("count", {})
            local_obj["total_games"] = cnt.get("all")
            local_obj["total_wins"] = cnt.get("win")

    return count_updated

def verificar_inatividade_time(user_list):
    now = datetime.now(timezone.utc)
    limit = timedelta(days=TEAM_INACTIVITY_DAYS)
    
    for p in user_list:
        # Ignora quem já está fechado ou banido
        if p.get("status") == "banned" or p.get("closed_account") is True:
            continue

        ls_str = p.get("last_seen_team_date")
        if ls_str:
            try:
                ls_dt = datetime.fromisoformat(ls_str.replace('Z', '+00:00'))
                if (now - ls_dt) > limit:
                    p["status"] = "inactive"
                elif p.get("status") == "inactive":
                    p["status"] = "active"
            except: pass

def main():
    print("--- ATUALIZAÇÃO MENSAL: LÓGICA INVERTIDA ---")
    start_time = time.time()

    # 1. Carregar
    db_players = carregar_json(FILES_CONFIG["players"])
    db_lurkers = carregar_json(FILES_CONFIG["lurkers"])
    db_ex = carregar_json(FILES_CONFIG["ex_members"])

    master_map = {}
    ids_to_fetch = []

    def indexar_lista(lista):
        for p in lista:
            uid = p.get("id_lichess")
            if not uid: uid = p.get("username")
            if uid:
                uid = uid.lower()
                p["id_lichess"] = uid
                master_map[uid] = p
                ids_to_fetch.append(uid)

    print("📂 Carregando dados...")
    indexar_lista(db_players)
    indexar_lista(db_lurkers)
    indexar_lista(db_ex)
    
    unique_ids = list(set(ids_to_fetch))
    chunks = list(chunk_list(unique_ids, BATCH_SIZE))
    print(f"📡 Verificando {len(unique_ids)} usuários em {len(chunks)} lotes...")

    total_processed = 0
    for i, batch in enumerate(chunks):
        print(f"   Lote {i+1}... ", end="")
        try:
            resp = requests.post("https://lichess.org/api/users", data=','.join(batch))
            
            if resp.status_code == 200:
                data = resp.json()
                # AQUI ESTÁ A MUDANÇA: Passamos o batch para marcar todos como fechados antes
                processar_lote_invertido(data, master_map, batch)
                print(f"Ok. (Retorno: {len(data)} / Lote: {len(batch)})")
                total_processed += len(data)
            else:
                print(f"Erro API: {resp.status_code} - Lote ignorado (ninguém alterado)")
                
        except Exception as e:
            print(f"Erro Conexão: {e}")
        
        time.sleep(1.2)

    # 3. Regras de Negócio Locais
    print("⏳ Atualizando inatividade...")
    verificar_inatividade_time(db_players)

    # 4. Salvar
    print("💾 Salvando...")
    salvar_json(FILES_CONFIG["players"], db_players)
    salvar_json(FILES_CONFIG["lurkers"], db_lurkers)
    salvar_json(FILES_CONFIG["ex_members"], db_ex)
    
    # Metadados
    all_users = db_players + db_lurkers + db_ex
    salvar_json(BANNED_FILE, [u["username"] for u in all_users if u.get("status") == "banned"])
    salvar_json(INACTIVE_FILE, [u["username"] for u in all_users if u.get("status") == "inactive"])
    salvar_json(METADATA_FILE, {"last_api_check": datetime.now(timezone.utc).isoformat()})

    print(f"✅ Feito em {(time.time() - start_time)/60:.2f} min.")

if __name__ == "__main__":
    main()