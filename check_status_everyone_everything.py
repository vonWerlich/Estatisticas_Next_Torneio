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

# Garante que a pasta existe
if not os.path.exists(DATA_DIR_PLAYERS):
    os.makedirs(DATA_DIR_PLAYERS)

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

def marcar_lote_como_fechado(master_map, requested_batch_ids):
    """
    PASSO 1: O MASSACRE
    Marca preventivamente todos os IDs do lote atual como 'closed_account = True'.
    Isso acontece ANTES da requisição. Se a requisição falhar, eles ficam como fechados.
    """
    for req_id in requested_batch_ids:
        local_obj = master_map.get(req_id)
        if local_obj:
            local_obj["closed_account"] = True

def atualizar_com_resposta_api(api_users, master_map):
    """
    PASSO 2: A RESSURREIÇÃO
    Processa apenas quem a API retornou com sucesso.
    """
    count_updated = 0
    
    for api_data in api_users:
        uid = api_data.get("id") # Lichess retorna ID em minúsculo
        local_obj = master_map.get(uid)
        
        if local_obj:
            count_updated += 1
            
            # Checa se a API diz explicitamente que está fechada (campo 'disabled')
            esta_desativada = api_data.get("disabled", False)
            
            # Se a conta existe e NÃO está desativada, nós "abrimos" ela novamente.
            # Se 'disabled' for True, mantemos o closed_account=True definido no Passo 1.
            if not esta_desativada:
                local_obj["closed_account"] = False

            # --- Atualização de Dados ---
            local_obj["username"] = api_data.get("username", local_obj.get("username"))
            local_obj["title"] = api_data.get("title")
            local_obj["country"] = api_data.get("profile", {}).get("country")
            
            # Status Banido (tosViolation)
            if api_data.get("tosViolation"):
                local_obj["status"] = "banned"
            else:
                # Se estava banido antes mas a API não diz mais nada, volta para active
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
                # Trata formato ISO com ou sem Z
                ls_dt = datetime.fromisoformat(ls_str.replace('Z', '+00:00'))
                if (now - ls_dt) > limit:
                    p["status"] = "inactive"
                elif p.get("status") == "inactive":
                    p["status"] = "active"
            except: pass

def main():
    print("--- ATUALIZAÇÃO MENSAL: LÓGICA CORRIGIDA (User-Agent + Ordem Certa) ---")
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

    # Cabeçalho para evitar bloqueio da API (User-Agent é obrigatório/boa prática)
    headers = {
        'User-Agent': 'ScriptVerificacaoStatus/1.0 (admin_contact: seu_email@exemplo.com)',
        'Accept': 'application/json'
    }

    total_processed = 0
    
    for i, batch in enumerate(chunks):
        print(f"   Lote {i+1}... ", end="")
        
        # --- MUDANÇA CRUCIAL: Marca como fechado ANTES da requisição ---
        marcar_lote_como_fechado(master_map, batch)

        try:
            resp = requests.post(
                "https://lichess.org/api/users", 
                data=','.join(batch),
                headers=headers
            )
            
            if resp.status_code == 200:
                data = resp.json()
                # Processa quem voltou vivo
                qtd_atualizados = atualizar_com_resposta_api(data, master_map)
                print(f"Ok. (Retorno API: {len(data)} / Atualizados: {qtd_atualizados})")
                total_processed += len(data)
            else:
                # Se der erro, eles continuam marcados como closed=True (segurança)
                print(f"Erro API: {resp.status_code} - Mantendo lote como fechado/indisponível.")
                
        except Exception as e:
            print(f"Erro Conexão: {e} - Mantendo lote como fechado/indisponível.")
        
        # Delay respeitoso para a API
        time.sleep(1.5)

    # 3. Regras de Negócio Locais (Inatividade do time)
    print("⏳ Atualizando inatividade por tempo...")
    verificar_inatividade_time(db_players)

    # 4. Salvar
    print("💾 Salvando arquivos...")
    salvar_json(FILES_CONFIG["players"], db_players)
    salvar_json(FILES_CONFIG["lurkers"], db_lurkers)
    salvar_json(FILES_CONFIG["ex_members"], db_ex)
    
    # Gerar Metadados Auxiliares
    all_users = db_players + db_lurkers + db_ex
    
    banned_list = [u["username"] for u in all_users if u.get("status") == "banned"]
    inactive_list = [u["username"] for u in all_users if u.get("status") == "inactive"]
    
    salvar_json(BANNED_FILE, banned_list)
    salvar_json(INACTIVE_FILE, inactive_list)
    
    salvar_json(METADATA_FILE, {
        "last_api_check": datetime.now(timezone.utc).isoformat(),
        "total_checked": len(unique_ids),
        "total_active_api": total_processed
    })

    print(f"✅ Processo finalizado em {(time.time() - start_time)/60:.2f} min.")

if __name__ == "__main__":
    main()