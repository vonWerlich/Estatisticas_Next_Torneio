import os
import requests
import json
import sys
from datetime import datetime, timezone

# --- CONFIGURAÇÃO ---
TEAM_ID = "next-nucleo-de-estudos-em-xadrez--tecnologias"
DATA_DIR_TORNEIOS = "torneiosnew"
DATA_DIR_PLAYERS = "player_data"

PLAYER_DB_FILE = os.path.join(DATA_DIR_PLAYERS, "players.json")
PARTICIPANTS_MAP_FILE = os.path.join(DATA_DIR_PLAYERS, "tournament_participants.json")
# Data de corte para leitura exaustiva de jogos (Fuso -03:00)
# Mantida para garantir consistência com a lógica de "Ghost Hunting"
DEFAULT_GHOST_CHECK_CUTOFF = "2020-05-08T18:30:00-03:00"

os.makedirs(DATA_DIR_TORNEIOS, exist_ok=True)
os.makedirs(DATA_DIR_PLAYERS, exist_ok=True)

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

# --- FUNÇÕES AUXILIARES (I/O) ---

def carregar_json(filepath, default_value):
    if not os.path.exists(filepath): return default_value
    try:
        with open(filepath, "r", encoding="utf-8") as f: return json.load(f)
    except: return default_value

def salvar_json(filepath, data):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def converter_data_para_iso(data_valor):
    if data_valor is None: return None
    if isinstance(data_valor, (int, float)):
        try: return datetime.fromtimestamp(data_valor / 1000, tz=timezone.utc).isoformat()
        except: return None
    if isinstance(data_valor, str):
        try:
            dt = datetime.fromisoformat(data_valor.replace('Z', '+00:00'))
            if dt.tzinfo is None: dt = dt.replace(tzinfo=timezone.utc)
            return dt.isoformat()
        except: return None
    return None

# --- CORE LÓGICA: EXTRAÇÃO E PROCESSAMENTO ---

def extrair_jogadores_dos_games(games_file_path):
    """
    Lê o ndjson de jogos e retorna um SET com os usernames únicos.
    Vital para encontrar jogadores que não aparecem no results.json.
    """
    players_in_games = set()
    if not os.path.exists(games_file_path): return players_in_games
    try:
        with open(games_file_path, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip(): continue
                try:
                    game = json.loads(line)
                    # Tenta extrair White
                    w = game.get('players', {}).get('white', {}).get('user', {}).get('name')
                    if w: players_in_games.add(w)
                    # Tenta extrair Black
                    b = game.get('players', {}).get('black', {}).get('user', {}).get('name')
                    if b: players_in_games.add(b)
                except: continue
    except Exception as e:
        print(f"⚠ Erro ao ler jogos em {games_file_path}: {e}")
    return players_in_games

def _upsert_player(username, t_date_iso, t_date_dt, players_db, username_to_id_map, next_player_id):
    """Cria ou atualiza metadados do jogador no DB (First Seen / Last Seen)."""
    player_id = username_to_id_map.get(username)

    if player_id is None:
        player_id = next_player_id
        new_player = {
            "id": player_id, 
            "username": username,
            "first_seen_team_date": t_date_iso,
            "last_seen_team_date": t_date_iso,
            "last_seen_api_timestamp": None, 
            "status": "active"
        }
        players_db.append(new_player)
        username_to_id_map[username] = player_id
    else:
        player_obj = next((p for p in players_db if p['id'] == player_id), None)
        if player_obj and t_date_dt:
            # Atualiza First Seen (se a data nova for menor)
            curr_first = player_obj.get("first_seen_team_date")
            if not curr_first:
                player_obj["first_seen_team_date"] = t_date_iso
            else:
                try:
                    if t_date_dt < datetime.fromisoformat(curr_first.replace('Z', '+00:00')):
                        player_obj["first_seen_team_date"] = t_date_iso
                except: pass
            
            # Atualiza Last Seen (se a data nova for maior)
            curr_last = player_obj.get("last_seen_team_date")
            if not curr_last:
                player_obj["last_seen_team_date"] = t_date_iso
            else:
                try:
                    if t_date_dt > datetime.fromisoformat(curr_last.replace('Z', '+00:00')):
                        player_obj["last_seen_team_date"] = t_date_iso
                except: pass
            
    return player_id

def update_player_databases(t_id, t_date_ms, results_data, players_db, username_to_id_map, participants_map, games_file_path=None, read_games=False):
    """
    Atualiza players.json combinando Results e Games.
    Esta função contém a correção crítica para jogadores 'fantasmas' ou não classificados.
    """
    t_date_iso = converter_data_para_iso(t_date_ms)
    t_date_dt = None
    if t_date_iso:
        try: t_date_dt = datetime.fromisoformat(t_date_iso.replace('Z', '+00:00'))
        except: pass

    # --- UNIÃO DE LISTAS ---
    all_usernames = set()
    
    # 1. Adiciona da Classificação (Results)
    if results_data:
        for entry in results_data:
            u = entry.get("username")
            if u: all_usernames.add(u)
            
    # 2. Adiciona dos Jogos (Se permitido e arquivo existir)
    if read_games and games_file_path:
        games_users = extrair_jogadores_dos_games(games_file_path)
        count_before = len(all_usernames)
        all_usernames.update(games_users)
        diff = len(all_usernames) - count_before
        if diff > 0:
            print(f"  -> 👻 +{diff} jogadores recuperados dos jogos (não classificados).")

    if not all_usernames: 
        return

    # 3. Atualiza DB
    participant_ids = []
    if players_db: next_player_id = max([p['id'] for p in players_db]) + 1
    else: next_player_id = 1
    
    for username in all_usernames:
        p_id = _upsert_player(username, t_date_iso, t_date_dt, players_db, username_to_id_map, next_player_id)
        if p_id == next_player_id: next_player_id += 1
        participant_ids.append(p_id)

    # AQUI ESTÁ A "FLAG": Se o ID do torneio entrar no mapa, ele foi processado.
    participants_map[t_id] = list(set(participant_ids))
    print(f"  -> Processamento concluído: {len(participant_ids)} participantes mapeados.")

# --- COMUNICAÇÃO COM API ---

def fetch_all_team_tournaments(team_id):
    """Busca APENAS os últimos torneios da API (default do Lichess)."""
    urls = [(f"https://lichess.org/api/team/{team_id}/arena", "arena"),
            (f"https://lichess.org/api/team/{team_id}/swiss", "swiss")]
    tournaments = []
    print("\n📡 Buscando lista de torneios recentes da API...")
    for url, tipo in urls:
        try:
            resp = requests.get(url, stream=True)
            resp.raise_for_status()
            for line in resp.iter_lines():
                if not line: continue
                d = json.loads(line.decode("utf-8"))
                tournaments.append({
                    "id": d.get("id"), 
                    "fullName": d.get("fullName","?"), 
                    "type": tipo, 
                    "startsAt": d.get("startsAt")
                })
        except Exception as e: print(f"⚠ Erro na API {tipo}: {e}")
    return tournaments

def download_tournament_files(t_info, directory):
    tid = t_info["id"]
    base_url = f"https://lichess.org/api/tournament/{tid}" if t_info["type"] == "arena" else f"https://lichess.org/api/swiss/{tid}"
    print(f"\n📥 Baixando {tid} ({t_info.get('fullName')})...")
    try:
        # 1. Info
        info = requests.get(base_url).json()
        salvar_json(os.path.join(directory, f"{tid}_info.json"), info)
        
        # 2. Results (NDJSON -> List)
        res_txt = requests.get(f"{base_url}/results", headers={"Accept": "application/x-ndjson"}).text
        results = [json.loads(l) for l in res_txt.strip().split('\n') if l]
        salvar_json(os.path.join(directory, f"{tid}_results.json"), results)
        
        # 3. Games (NDJSON Stream)
        with requests.get(f"{base_url}/games", stream=True, headers={"Accept": "application/x-ndjson"}) as r, \
             open(os.path.join(directory, f"{tid}_games.ndjson"), "w", encoding="utf-8") as f:
            for line in r.iter_lines(): 
                if line: f.write(line.decode('utf-8') + '\n')
        
        return info, results
    except Exception as e:
        print(f"!!! Erro ao baixar {tid}: {e}")
        return None, None

def sync_team_members(team_id, players_db, username_to_id_map):
    """
    Sincroniza membros da equipe. Importante para pegar quem se inscreveu
    mas nunca jogou torneio (lurkers).
    """
    print(f"\n👥 Sincronizando lista de membros da equipe...")
    url = f"https://lichess.org/api/team/{team_id}/users"
    added = 0
    if players_db: next_id = max([p['id'] for p in players_db]) + 1
    else: next_id = 1
    
    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            for line in r.iter_lines():
                if not line: continue
                m = json.loads(line.decode('utf-8'))
                u = m.get("username")
                if u and u not in username_to_id_map:
                    players_db.append({
                        "id": next_id, "username": u,
                        "first_seen_team_date": None, "last_seen_team_date": None,
                        "last_seen_api_timestamp": m.get("seenAt"), "status": "active"
                    })
                    username_to_id_map[u] = next_id
                    next_id += 1
                    added += 1
    except Exception as e: print(f"⚠ Erro ao sync membros: {e}")
    
    if added > 0: print(f"✅ {added} novos membros (sem torneios) adicionados.")
    return added > 0

# --- MAIN: EXECUÇÃO LEVE ---

def run_update_lite():
    print("--- ATUALIZAÇÃO INCREMENTAL DE TORNEIOS (LITE) ---")
    
    # 1. Carrega Estado Atual
    players_db = carregar_json(PLAYER_DB_FILE, [])
    participants_map = carregar_json(PARTICIPANTS_MAP_FILE, {})
    username_to_id_map = {p['username']: p['id'] for p in players_db}
    
    # Prepara data de corte (Segurança)
    try: cutoff_dt = datetime.fromisoformat(DEFAULT_GHOST_CHECK_CUTOFF.replace('Z', '+00:00'))
    except: cutoff_dt = datetime.now(timezone.utc)
    
    # 2. Busca API e Filtra Novos
    all_api_tournaments = fetch_all_team_tournaments(TEAM_ID)
    
    # AQUI ESTÁ A LÓGICA DE PERFORMANCE:
    # Só processa se o ID do torneio NÃO estiver no mapa de participantes.
    # O mapa serve como a "flag" de processado.
    new_tournaments = [t for t in all_api_tournaments if t["id"] not in participants_map]
    
    changes = False
    
    if new_tournaments:
        print(f"✨ {len(new_tournaments)} novos torneios encontrados.")
        
        for t_info in new_tournaments:
            tid = t_info["id"]
            
            # Download
            info, results = download_tournament_files(t_info, DATA_DIR_TORNEIOS)
            
            if info and results is not None:
                t_ms = info.get("startsAt")
                t_iso = converter_data_para_iso(t_ms)
                
                # Verifica data para ler jogos
                should_read_games = False
                if t_iso:
                    try: 
                        t_dt = datetime.fromisoformat(t_iso.replace('Z', '+00:00'))
                        if t_dt >= cutoff_dt: should_read_games = True
                    except: pass
                
                games_path = os.path.join(DATA_DIR_TORNEIOS, f"{tid}_games.ndjson")
                
                # Processa e Atualiza DB
                update_player_databases(
                    tid, t_ms, results, players_db, 
                    username_to_id_map, participants_map, 
                    games_file_path=games_path, 
                    read_games=should_read_games
                )
                changes = True
    else:
        print("✅ Nenhum torneio novo para baixar.")

    # 3. Sincroniza Membros (Sempre bom checar novas entradas na equipe)
    changes_members = sync_team_members(TEAM_ID, players_db, username_to_id_map)
    
    # 4. Salva apenas se houve mudança
    if changes or changes_members:
        print("💾 Salvando alterações no banco de dados...")
        salvar_json(PLAYER_DB_FILE, players_db)
        salvar_json(PARTICIPANTS_MAP_FILE, participants_map)
    else:
        print("✅ Dados já estavam atualizados.")
    
    print("🏁 Atualização concluída.")

if __name__ == "__main__":
    run_update_lite()