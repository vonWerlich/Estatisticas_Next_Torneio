import os
import json
import sys
from datetime import datetime, timezone

# --- CONFIGURAÇÃO ---
DATA_DIR_TORNEIOS = "torneiosnew"
DATA_DIR_PLAYERS = "player_data"
PLAYER_DB_FILE = os.path.join(DATA_DIR_PLAYERS, "players.json")
PARTICIPANTS_MAP_FILE = os.path.join(DATA_DIR_PLAYERS, "tournament_participants.json")

# Data de corte para ler os jogos (games.ndjson) - Fuso -03:00
DEFAULT_GHOST_CHECK_CUTOFF = "2020-05-08T18:30:00-03:00"

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

# --- FUNÇÕES UTILITÁRIAS (Replicadas para manter consistência) ---
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
    return None

def extrair_jogadores_dos_games(games_file_path):
    players = set()
    if not os.path.exists(games_file_path): return players
    try:
        with open(games_file_path, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip(): continue
                try:
                    g = json.loads(line)
                    w = g.get('players', {}).get('white', {}).get('user', {}).get('name')
                    b = g.get('players', {}).get('black', {}).get('user', {}).get('name')
                    if w: players.add(w)
                    if b: players.add(b)
                except: continue
    except: pass
    return players

def _upsert_player(username, t_date_iso, t_date_dt, players_db, username_to_id_map, next_player_id):
    pid = username_to_id_map.get(username)
    if pid is None:
        pid = next_player_id
        players_db.append({
            "id": pid, "username": username,
            "first_seen_team_date": t_date_iso, "last_seen_team_date": t_date_iso,
            "last_seen_api_timestamp": None, "status": "active"
        })
        username_to_id_map[username] = pid
    else:
        # Lógica de atualização de datas (simplificada para o exemplo)
        p = next((x for x in players_db if x['id'] == pid), None)
        if p and t_date_dt:
            # Atualiza First Seen
            try:
                curr = p.get("first_seen_team_date")
                if not curr or t_date_dt < datetime.fromisoformat(curr.replace('Z','+00:00')):
                    p["first_seen_team_date"] = t_date_iso
            except: pass
            # Atualiza Last Seen
            try:
                curr = p.get("last_seen_team_date")
                if not curr or t_date_dt > datetime.fromisoformat(curr.replace('Z','+00:00')):
                    p["last_seen_team_date"] = t_date_iso
            except: pass
    return pid

def run_historical_fix():
    print("--- INICIANDO PROCESSAMENTO DE HISTÓRICO LOCAL ---")
    
    players_db = carregar_json(PLAYER_DB_FILE, [])
    participants_map = carregar_json(PARTICIPANTS_MAP_FILE, {})
    username_to_id_map = {p['username']: p['id'] for p in players_db}
    
    # Prepara data de corte
    try: cutoff_dt = datetime.fromisoformat(DEFAULT_GHOST_CHECK_CUTOFF.replace('Z', '+00:00'))
    except: cutoff_dt = datetime.now(timezone.utc)

    # Lista todos os IDs na pasta
    files_on_disk = [f.split("_")[0] for f in os.listdir(DATA_DIR_TORNEIOS) if f.endswith("_info.json")]
    
    # Filtra apenas os que NÃO estão no mapa (sua "flag")
    unprocessed_ids = [tid for tid in files_on_disk if tid not in participants_map]
    
    print(f"📂 Total de arquivos na pasta: {len(files_on_disk)}")
    print(f"⚙️ Torneios pendentes de processamento: {len(unprocessed_ids)}")
    
    if not unprocessed_ids:
        print("✅ Nada a fazer. Histórico está sincronizado.")
        return

    next_player_id = max([p['id'] for p in players_db] + [0]) + 1
    
    for tid in unprocessed_ids:
        print(f"processando: {tid}...", end="")
        info = carregar_json(os.path.join(DATA_DIR_TORNEIOS, f"{tid}_info.json"), {})
        results = carregar_json(os.path.join(DATA_DIR_TORNEIOS, f"{tid}_results.json"), [])
        
        t_ms = info.get("startsAt")
        t_iso = converter_data_para_iso(t_ms)
        t_dt = None
        if t_iso:
            try: t_dt = datetime.fromisoformat(t_iso.replace('Z', '+00:00'))
            except: pass

        # Decide se lê jogos
        read_games = False
        if t_dt and t_dt >= cutoff_dt:
            read_games = True
            
        # Coleta users
        users = set()
        if results:
            users.update([r.get("username") for r in results if r.get("username")])
            
        if read_games:
            g_path = os.path.join(DATA_DIR_TORNEIOS, f"{tid}_games.ndjson")
            users.update(extrair_jogadores_dos_games(g_path))
            
        # Atualiza DB
        p_ids = []
        for u in users:
            pid = _upsert_player(u, t_iso, t_dt, players_db, username_to_id_map, next_player_id)
            if pid == next_player_id: next_player_id += 1
            p_ids.append(pid)
            
        participants_map[tid] = list(set(p_ids))
        print(f" ok ({len(users)} jogadores)")

    print("💾 Salvando alterações...")
    salvar_json(PLAYER_DB_FILE, players_db)
    salvar_json(PARTICIPANTS_MAP_FILE, participants_map)
    print("🏁 Histórico corrigido com sucesso!")

if __name__ == "__main__":
    run_historical_fix()