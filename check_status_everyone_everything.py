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

TEAM_ID = "next-nucleo-de-estudos-em-xadrez--tecnologias"
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

def processar_lote(api_users, master_map, requested_batch_ids):
    """
    Atualiza dados de quem existe E marca closed_account=True em quem sumiu.
    """
    count_updated = 0
    received_ids = set()
    
    # 1. ATUALIZA QUEM O LICHESS RESPONDEU
    for api_data in api_users:
        uid = api_data.get("id") # ID sempre vem minúsculo da API
        received_ids.add(uid)
        local_obj = master_map.get(uid)
        
        if local_obj:
            count_updated += 1
            
            # --- DEFINIÇÃO DA FLAG (TRUE/FALSE) ---
            # Se 'disabled': true, a conta está fechada.
            # Se 'disabled' não vier, assumimos False (Aberta).
            local_obj["closed_account"] = api_data.get("disabled", False)

            # Atualiza dados cadastrais
            local_obj["username"] = api_data.get("username")
            local_obj["title"] = api_data.get("title")
            local_obj["country"] = api_data.get("profile", {}).get("country")
            
            # --- STATUS (Banidos têm prioridade) ---
            if api_data.get("tosViolation"):
                local_obj["status"] = "banned"
            else:
                # Se não é banido, limpamos o status 'banned' se existir
                if local_obj.get("status") == "banned":
                    local_obj["status"] = "active"
                
            local_obj["last_seen_api_timestamp"] = api_data.get("seenAt")
            
            # Ratings & Stats
            perfs = api_data.get("perfs", {})
            local_obj["rating_blitz"] = perfs.get("blitz", {}).get("rating")
            local_obj["rating_rapid"] = perfs.get("rapid", {}).get("rating")
            local_obj["rating_bullet"] = perfs.get("bullet", {}).get("rating")
            local_obj["rating_puzzle"] = perfs.get("puzzle", {}).get("rating")
            
            cnt = api_data.get("count", {})
            local_obj["total_games"] = cnt.get("all")
            local_obj["total_wins"] = cnt.get("win")

    # 2. MARCA QUEM O LICHESS IGNOROU (CONTAS DELETADAS)
    # Se pedimos o ID e ele não veio na resposta, a conta não existe mais.
    for req_id in requested_batch_ids:
        if req_id not in received_ids:
            local_obj = master_map.get(req_id)
            if local_obj:
                # FORÇA A FLAG PARA TRUE
                local_obj["closed_account"] = True
                
                # Se não veio nada, não temos ratings novos, mantemos os velhos.

    return count_updated

def verificar_inatividade_time(user_list):
    """Marca status 'inactive' apenas para quem está com conta aberta e limpa."""
    now = datetime.now(timezone.utc)
    limit = timedelta(days=TEAM_INACTIVITY_DAYS)
    
    for p in user_list:
        # Só marcamos inatividade se a conta não estiver banida nem fechada
        if p.get("status") != "banned" and p.get("closed_account") is not True:
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
    print("--- ATUALIZAÇÃO MENSAL (LÓGICA CORRIGIDA) ---")
    start_time = time.time()

    # 1. Carregar Tudo
    db_players = carregar_json(FILES_CONFIG["players"])
    db_lurkers = carregar_json(FILES_CONFIG["lurkers"])
    db_ex = carregar_json(FILES_CONFIG["ex_members"])

    master_map = {}
    ids_to_fetch = []

    # --- CORREÇÃO AQUI: INICIALIZAÇÃO SEGURA ---
    def indexar_lista(lista):
        for p in lista:
            uid = p.get("id_lichess")
            if not uid: uid = p.get("username")
            if uid:
                uid = uid.lower()
                p["id_lichess"] = uid
                
                # Garante que o campo closed_account exista como False por padrão
                # Se já for True, mantém True. Se não existir, vira False.
                if "closed_account" not in p:
                    p["closed_account"] = False
                
                master_map[uid] = p
                ids_to_fetch.append(uid)

    print("📂 Carregando e Inicializando Dados...")
    indexar_lista(db_players)
    indexar_lista(db_lurkers)
    indexar_lista(db_ex)
    
    unique_ids = list(set(ids_to_fetch))
    print(f"   Total para verificar: {len(unique_ids)}")

    # 2. Consultar API
    chunks = list(chunk_list(unique_ids, BATCH_SIZE))
    print(f"\n📡 Verificando API ({len(chunks)} lotes)...")

    for i, batch in enumerate(chunks):
        print(f"   Lote {i+1}... ", end="")
        try:
            resp = requests.post("https://lichess.org/api/users", data=','.join(batch))
            
            if resp.status_code == 200:
                data = resp.json()
                processar_lote(data, master_map, batch)
                print(f"Ok. (Retorno: {len(data)}/{len(batch)})")
            else:
                print(f"Erro API: {resp.status_code}")
                
        except Exception as e:
            print(f"Erro Conexão: {e}")
        
        time.sleep(1.2)

    # 3. Verificar Inatividade
    verificar_inatividade_time(db_players)

    # 4. Salvar
    print("\n💾 Salvando arquivos...")
    salvar_json(FILES_CONFIG["players"], db_players)
    salvar_json(FILES_CONFIG["lurkers"], db_lurkers)
    salvar_json(FILES_CONFIG["ex_members"], db_ex)
    
    # Relatórios
    all_users = db_players + db_lurkers + db_ex
    
    # Contagem corrigida usando a flag
    closed_count = sum(1 for u in all_users if u.get("closed_account") is True)
    banned_count = sum(1 for u in all_users if u.get("status") == "banned")
    inactive_count = sum(1 for u in all_users if u.get("status") == "inactive")

    salvar_json(BANNED_FILE, [u["username"] for u in all_users if u.get("status") == "banned"])
    salvar_json(INACTIVE_FILE, [u["username"] for u in all_users if u.get("status") == "inactive"])
    
    salvar_json(METADATA_FILE, {"last_api_check": datetime.now(timezone.utc).isoformat()})

    duration = (time.time() - start_time) / 60
    print(f"✅ Concluído em {duration:.2f} min.")
    print(f"   - Contas Fechadas: {closed_count}")
    print(f"   - Banidos: {banned_count}")
    print(f"   - Inativos: {inactive_count}")

if __name__ == "__main__":
    main()