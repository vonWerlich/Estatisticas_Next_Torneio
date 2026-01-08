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

def processar_lote(api_users, master_map, requested_batch_ids):
    """
    Lógica 'Agressiva' para detectar contas fechadas.
    """
    count_updated = 0
    received_ids = set()
    
    # 1. PROCESSAR QUEM O LICHESS RESPONDEU
    for api_data in api_users:
        uid = api_data.get("id")
        received_ids.add(uid)
        local_obj = master_map.get(uid)
        
        if local_obj:
            count_updated += 1
            
            # --- DETECTOR DE ZUMBIS (Respondeu, mas veio vazio?) ---
            # Contas fechadas as vezes retornam sem 'perfs' (ratings) e sem 'createdAt'
            tem_ratings = bool(api_data.get("perfs"))
            tem_criacao = bool(api_data.get("createdAt"))
            esta_desativada = api_data.get("disabled", False)

            # Se estiver desativada OU (não tem ratings E não tem data de criação) -> FECHADA
            if esta_desativada or (not tem_ratings and not tem_criacao):
                local_obj["closed_account"] = True
            else:
                local_obj["closed_account"] = False

            # --- ATUALIZAÇÃO DE DADOS ---
            local_obj["username"] = api_data.get("username", local_obj.get("username"))
            local_obj["title"] = api_data.get("title")
            local_obj["country"] = api_data.get("profile", {}).get("country")
            
            # --- STATUS (Banidos têm prioridade) ---
            if api_data.get("tosViolation"):
                local_obj["status"] = "banned"
            else:
                # Se não é banido, removemos status 'banned' antigo
                if local_obj.get("status") == "banned":
                    local_obj["status"] = "active"
                
            local_obj["last_seen_api_timestamp"] = api_data.get("seenAt")
            local_obj["created_at"] = api_data.get("createdAt")
            
            # Ratings & Stats
            perfs = api_data.get("perfs", {})
            local_obj["rating_blitz"] = perfs.get("blitz", {}).get("rating")
            local_obj["rating_rapid"] = perfs.get("rapid", {}).get("rating")
            local_obj["rating_bullet"] = perfs.get("bullet", {}).get("rating")
            local_obj["rating_puzzle"] = perfs.get("puzzle", {}).get("rating")
            
            cnt = api_data.get("count", {})
            local_obj["total_games"] = cnt.get("all")
            local_obj["total_wins"] = cnt.get("win")

    # 2. DETECTOR DE FANTASMAS (Quem eu pedi e NÃO veio)
    # Se o ID foi solicitado no lote, mas não está em 'received_ids', a conta não existe.
    for req_id in requested_batch_ids:
        if req_id not in received_ids:
            local_obj = master_map.get(req_id)
            if local_obj:
                # Marca explicitamente como fechada
                local_obj["closed_account"] = True
                
                # Se não tem ratings (nunca teve), garante que fiquem null ou 0
                # Isso limpa a sujeira visual
                if not local_obj.get("rating_blitz"):
                    local_obj["status"] = "closed" # Força status closed visualmente também

    return count_updated

def verificar_inatividade_time(user_list):
    """Marca inatividade apenas em contas VÁLIDAS."""
    now = datetime.now(timezone.utc)
    limit = timedelta(days=TEAM_INACTIVITY_DAYS)
    
    for p in user_list:
        # Pula banidos e fechados
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
    print("--- ATUALIZAÇÃO MENSAL: LIMPEZA PROFUNDA ---")
    start_time = time.time()

    # 1. Carregar Dados
    db_players = carregar_json(FILES_CONFIG["players"])
    db_lurkers = carregar_json(FILES_CONFIG["lurkers"])
    db_ex = carregar_json(FILES_CONFIG["ex_members"])

    master_map = {}
    ids_to_fetch = []

    def indexar_lista(lista, nome_arquivo):
        print(f"   Indexando {nome_arquivo} ({len(lista)} registros)...")
        for p in lista:
            uid = p.get("id_lichess")
            if not uid: uid = p.get("username")
            if uid:
                uid = uid.lower()
                p["id_lichess"] = uid
                
                # INICIALIZAÇÃO CORRETIVA:
                # Se não tem o campo, cria como False.
                # Se já tem True, mantém.
                if "closed_account" not in p:
                    p["closed_account"] = False
                
                master_map[uid] = p
                ids_to_fetch.append(uid)

    print("📂 Preparando memória...")
    indexar_lista(db_players, "players")
    indexar_lista(db_lurkers, "lurkers")
    indexar_lista(db_ex, "ex_members")
    
    unique_ids = list(set(ids_to_fetch))
    print(f"   Total de IDs únicos: {len(unique_ids)}")

    # 2. Consultar API
    chunks = list(chunk_list(unique_ids, BATCH_SIZE))
    print(f"\n📡 Consultando Lichess em {len(chunks)} lotes...")

    total_closed_detected = 0

    for i, batch in enumerate(chunks):
        print(f"   Lote {i+1}... ", end="")
        try:
            resp = requests.post("https://lichess.org/api/users", data=','.join(batch))
            
            if resp.status_code == 200:
                data = resp.json()
                processar_lote(data, master_map, batch)
                print(f"Ok. (Retornados: {len(data)} / Pedidos: {len(batch)})")
                
                # Diferença = Contas Fechadas
                diff = len(batch) - len(data)
                if diff > 0:
                    total_closed_detected += diff
            else:
                print(f"Erro API: {resp.status_code}")
                
        except Exception as e:
            print(f"Erro Conexão: {e}")
        
        time.sleep(1.2) # Pausa para não tomar Rate Limit

    print(f"\n💀 Contas fantasmas detectadas e fechadas neste ciclo: {total_closed_detected}")

    # 3. Verificar Inatividade (Só nos ativos)
    print("⏳ Verificando inatividade temporal...")
    verificar_inatividade_time(db_players)

    # 4. Salvar
    print("💾 Salvando arquivos limpos...")
    salvar_json(FILES_CONFIG["players"], db_players)
    salvar_json(FILES_CONFIG["lurkers"], db_lurkers)
    salvar_json(FILES_CONFIG["ex_members"], db_ex)
    
    # Gerar listas auxiliares para o site
    all_users = db_players + db_lurkers + db_ex
    
    # Agora a contagem deve bater
    banned_names = [u["username"] for u in all_users if u.get("status") == "banned"]
    inactive_names = [u["username"] for u in all_users if u.get("status") == "inactive"]
    
    salvar_json(BANNED_FILE, banned_names)
    salvar_json(INACTIVE_FILE, inactive_names)
    salvar_json(METADATA_FILE, {"last_api_check": datetime.now(timezone.utc).isoformat()})

    duration = (time.time() - start_time) / 60
    print(f"✅ Concluído em {duration:.2f} min.")

if __name__ == "__main__":
    main()