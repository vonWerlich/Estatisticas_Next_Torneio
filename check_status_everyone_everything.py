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

# Arquivos que serão preservados e atualizados
FILES_CONFIG = {
    "players": os.path.join(DATA_DIR_PLAYERS, "players.json"),
    "lurkers": os.path.join(DATA_DIR_PLAYERS, "lurkers.json"),
    "ex_members": os.path.join(DATA_DIR_PLAYERS, "ex_members.json")
}

# Arquivos de saída auxiliar (apenas para consulta rápida)
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
    Atualiza dados e define a flag 'closed_account' (True/False).
    """
    count_updated = 0
    received_ids = set()
    
    # 1. ATUALIZAÇÃO (Para quem a conta respondeu na API)
    for api_data in api_users:
        uid = api_data.get("id")
        received_ids.add(uid)
        local_obj = master_map.get(uid)
        
        if local_obj:
            count_updated += 1
            
            # --- ATUALIZAÇÃO DO CAMPO NOVO (BOOL) ---
            # Se vier 'disabled': true na API, a conta está fechada.
            # Se não vier ou for false, a conta está aberta.
            local_obj["closed_account"] = api_data.get("disabled", False)

            # --- DADOS CADASTRAIS ---
            local_obj["username"] = api_data.get("username")
            local_obj["title"] = api_data.get("title")
            local_obj["country"] = api_data.get("profile", {}).get("country")
            
            # --- LÓGICA DE STATUS (Mantemos para Banned/Inactive) ---
            # Se closed_account for True, o status é secundário, mas podemos ajustar se quiser.
            # Aqui focamos em detectar Banimento.
            if api_data.get("tosViolation"):
                local_obj["status"] = "banned"
            else:
                # Se não é banido, definimos como active (o filtro de inativo roda depois)
                # Se a conta estiver fechada, você pode decidir se mantém status="active" 
                # e confia só no closed_account=True, ou muda o status também.
                # Vou deixar status="active" para não conflitarem, já que agora temos a flag bool.
                if local_obj.get("status") == "banned":
                    local_obj["status"] = "active"

            local_obj["last_seen_api_timestamp"] = api_data.get("seenAt")
            
            # Ratings & Stats
            perfs = api_data.get("perfs", {})
            local_obj["rating_blitz"] = perfs.get("blitz", {}).get("rating")
            local_obj["rating_rapid"] = perfs.get("rapid", {}).get("rating")
            local_obj["rating_bullet"] = perfs.get("bullet", {}).get("rating")
            
            cnt = api_data.get("count", {})
            local_obj["total_games"] = cnt.get("all")

    # 2. FLAGGING DE CONTAS DELETADAS (O Pulo do Gato)
    # Se pedimos o ID e ele não veio, a conta foi encerrada/deletada.
    for req_id in requested_batch_ids:
        if req_id not in received_ids:
            local_obj = master_map.get(req_id)
            if local_obj:
                # MARCA COMO FECHADA (True)
                local_obj["closed_account"] = True
                
                # Opcional: Se quiser limpar o status de banido caso a conta suma
                # local_obj["status"] = "active" 

    return count_updated

def verificar_inatividade_time(user_list):
    """Marca flag 'inactive' para quem sumiu dos torneios, mas mantém a conta aberta."""
    now = datetime.now(timezone.utc)
    limit = timedelta(days=TEAM_INACTIVITY_DAYS)
    
    for p in user_list:
        # Só marcamos inatividade se a conta ainda existe e é limpa
        if p.get("status") not in ["banned", "closed"]:
            ls_str = p.get("last_seen_team_date")
            if ls_str:
                try:
                    ls_dt = datetime.fromisoformat(ls_str.replace('Z', '+00:00'))
                    if (now - ls_dt) > limit:
                        p["status"] = "inactive" # Flag de Inatividade
                    elif p.get("status") == "inactive":
                        p["status"] = "active" # Voltou a jogar
                except: pass

def main():
    print("--- ATUALIZAÇÃO MENSAL: PRESERVANDO HISTÓRICO ---")
    start_time = time.time()

    # 1. Carregar Dados Históricos
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

    print("📂 Lendo registros históricos...")
    indexar_lista(db_players)
    indexar_lista(db_lurkers)
    indexar_lista(db_ex)
    
    unique_ids = list(set(ids_to_fetch))
    print(f"   Total de perfis monitorados: {len(unique_ids)}")

    # 2. Consultar API
    chunks = list(chunk_list(unique_ids, BATCH_SIZE))
    print(f"\n📡 Verificando status atual na API ({len(chunks)} lotes)...")

    for i, batch in enumerate(chunks):
        print(f"   Verificando lote {i+1}... ", end="")
        try:
            resp = requests.post("https://lichess.org/api/users", data=','.join(batch))
            
            if resp.status_code == 200:
                data = resp.json()
                processar_lote(data, master_map, batch)
                print(f"Ok. (Retorno: {len(data)}/{len(batch)})")
                # Se Retorno < Batch, a diferença são as contas fechadas detectadas.
            else:
                print(f"Erro API: {resp.status_code}")
                
        except Exception as e:
            print(f"Erro de conexão: {e}")
        
        time.sleep(1.2)

    # 3. Verificar Inatividade em Torneios
    verificar_inatividade_time(db_players)

    # 4. Salvar (Sobrescreve os arquivos JSON com os dados atualizados e flags novas)
    print("\n💾 Salvando histórico atualizado...")
    salvar_json(FILES_CONFIG["players"], db_players)
    salvar_json(FILES_CONFIG["lurkers"], db_lurkers)
    salvar_json(FILES_CONFIG["ex_members"], db_ex)
    
    # Relatórios rápidos
    all_users = db_players + db_lurkers + db_ex
    banned_names = [u["username"] for u in all_users if u.get("status") == "banned"]
    inactive_names = [u["username"] for u in all_users if u.get("status") == "inactive"]
    
    salvar_json(BANNED_FILE, banned_names)
    salvar_json(INACTIVE_FILE, inactive_names)
    
    salvar_json(METADATA_FILE, {"last_api_check": datetime.now(timezone.utc).isoformat()})

    duration = (time.time() - start_time) / 60
    print(f"✅ Processo concluído em {duration:.2f} min.")

if __name__ == "__main__":
    main()