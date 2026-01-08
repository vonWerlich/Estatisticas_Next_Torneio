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

# Arquivos que serão lidos e atualizados
FILES_CONFIG = {
    "players": os.path.join(DATA_DIR_PLAYERS, "players.json"),
    "lurkers": os.path.join(DATA_DIR_PLAYERS, "lurkers.json"),
    "ex_members": os.path.join(DATA_DIR_PLAYERS, "ex_members.json")
}

# Arquivos de relatório rápido (apenas listas de nomes)
BANNED_FILE = os.path.join(DATA_DIR_PLAYERS, "banned_players.json")
INACTIVE_FILE = os.path.join(DATA_DIR_PLAYERS, "inactive_players.json")
METADATA_FILE = os.path.join(DATA_DIR_PLAYERS, "status_metadata.json")

TEAM_INACTIVITY_DAYS = 547
BATCH_SIZE = 300 # Limite da API para POST

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

def processar_lote(api_users, master_map):
    """Atualiza os objetos locais com os dados vindos da API."""
    count_updated = 0
    
    for api_data in api_users:
        uid = api_data.get("id")
        local_obj = master_map.get(uid)
        
        if local_obj:
            count_updated += 1
            
            # --- 1. DADOS CADASTRAIS (Leves) ---
            local_obj["username"] = api_data.get("username")
            local_obj["title"] = api_data.get("title")
            local_obj["country"] = api_data.get("profile", {}).get("country")
            local_obj["location"] = api_data.get("profile", {}).get("location")
            # Ignoramos 'bio' e 'links' conforme solicitado
            
            # --- 2. STATUS (BAN / FECHADO) ---
            old_status = local_obj.get("status", "active")
            
            if api_data.get("tosViolation"):
                local_obj["status"] = "banned"
            elif api_data.get("disabled"):
                local_obj["status"] = "closed"
            elif old_status in ["banned", "closed"]:
                # Se estava banido mas a API não diz mais nada, reativa
                local_obj["status"] = "active"
                
            local_obj["last_seen_api_timestamp"] = api_data.get("seenAt")
            local_obj["created_at"] = api_data.get("createdAt")

            # --- 3. RATINGS & ESTATÍSTICAS ---
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
    """Marca como inativo quem não joga torneios do time há muito tempo."""
    now = datetime.now(timezone.utc)
    limit = timedelta(days=TEAM_INACTIVITY_DAYS)
    
    for p in user_list:
        # Só verifica inatividade se a conta estiver ativa
        if p.get("status") not in ["banned", "closed"]:
            ls_str = p.get("last_seen_team_date")
            if ls_str:
                try:
                    ls_dt = datetime.fromisoformat(ls_str.replace('Z', '+00:00'))
                    if (now - ls_dt) > limit:
                        p["status"] = "inactive"
                    elif p.get("status") == "inactive":
                        # Se jogou recentemente, reativa
                        p["status"] = "active"
                except: pass

def main():
    print("--- ATUALIZAÇÃO MENSAL UNIFICADA (STATUS + RATINGS) ---")
    start_time = time.time()

    # 1. Carregar tudo para memória
    db_players = carregar_json(FILES_CONFIG["players"])
    db_lurkers = carregar_json(FILES_CONFIG["lurkers"])
    db_ex = carregar_json(FILES_CONFIG["ex_members"])

    # Mapa Mestre: ID -> Objeto (para atualização rápida)
    master_map = {}
    ids_to_fetch = []

    # Função auxiliar para indexar
    def indexar_lista(lista):
        for p in lista:
            uid = p.get("id_lichess")
            if not uid: uid = p.get("username")
            if uid:
                uid = uid.lower()
                p["id_lichess"] = uid # Garante normalização
                master_map[uid] = p
                ids_to_fetch.append(uid)

    print("📂 Carregando bancos de dados...")
    indexar_lista(db_players)
    indexar_lista(db_lurkers)
    indexar_lista(db_ex)
    
    unique_ids = list(set(ids_to_fetch))
    print(f"   - Players: {len(db_players)}")
    print(f"   - Lurkers: {len(db_lurkers)}")
    print(f"   - Ex-membros: {len(db_ex)}")
    print(f"   - Total de IDs únicos para API: {len(unique_ids)}")

    # 2. Consultar API em Lotes
    chunks = list(chunk_list(unique_ids, BATCH_SIZE))
    print(f"\n📡 Iniciando consulta à API em {len(chunks)} lotes...")

    total_updates = 0
    for i, batch in enumerate(chunks):
        print(f"   Processando lote {i+1}/{len(chunks)}... ", end="")
        try:
            # POST request é muito mais eficiente que GET individual
            resp = requests.post("https://lichess.org/api/users", data=','.join(batch))
            
            if resp.status_code == 200:
                data = resp.json()
                n = processar_lote(data, master_map)
                total_updates += n
                print(f"Ok ({len(data)} usuários recebidos).")
            else:
                print(f"Erro API: {resp.status_code}")
                
        except Exception as e:
            print(f"Erro de conexão: {e}")
        
        time.sleep(1.2) # Pausa amigável

    # 3. Aplicar Regra de Inatividade do Time
    print("\n⏳ Verificando inatividade em torneios...")
    verificar_inatividade_time(db_players) 
    # Lurkers e Ex-membros não precisam dessa checagem pois não têm data de torneio recente

    # 4. Gerar Listas Rápidas (Banidos/Inativos) para o Site
    all_users = db_players + db_lurkers + db_ex
    banned_names = [u["username"] for u in all_users if u.get("status") == "banned"]
    inactive_names = [u["username"] for u in all_users if u.get("status") == "inactive"]

    # 5. Salvar Tudo
    print("\n💾 Salvando arquivos...")
    salvar_json(FILES_CONFIG["players"], db_players)
    salvar_json(FILES_CONFIG["lurkers"], db_lurkers)
    salvar_json(FILES_CONFIG["ex_members"], db_ex)
    
    salvar_json(BANNED_FILE, banned_names)
    salvar_json(INACTIVE_FILE, inactive_names)
    
    # Atualiza data da última checagem
    now_iso = datetime.now(timezone.utc).isoformat()
    salvar_json(METADATA_FILE, {"last_api_check": now_iso})

    duration = (time.time() - start_time) / 60
    print(f"✅ Concluído em {duration:.2f} minutos.")
    print(f"   - Banidos totais: {len(banned_names)}")
    print(f"   - Inativos totais: {len(inactive_names)}")

if __name__ == "__main__":
    main()