import os
import requests
import json
import sys
import time
from datetime import datetime, timedelta, timezone

# --- CONFIGURAÇÃO ---
TEAM_ID = "next-nucleo-de-estudos-em-xadrez--tecnologias"
DATA_DIR_TORNEIOS = "torneiosnew"
DATA_DIR_PLAYERS = "player_data"

PLAYER_DB_FILE = os.path.join(DATA_DIR_PLAYERS, "players.json")
PARTICIPANTS_MAP_FILE = os.path.join(DATA_DIR_PLAYERS, "tournament_participants.json")
BANNED_PLAYERS_FILE = os.path.join(DATA_DIR_PLAYERS, "banned_players.json")
INACTIVE_PLAYERS_FILE = os.path.join(DATA_DIR_PLAYERS, "inactive_players.json")
STATUS_METADATA_FILE = os.path.join(DATA_DIR_PLAYERS, "status_metadata.json")

# Data do primeiro torneio conforme solicitado. Torneios anteriores a isso seriam ignorados na checagem de fantasmas.
# Formato ISO 8601 com Fuso Horário (-03:00)
DEFAULT_GHOST_CHECK_CUTOFF = "2020-05-08T18:30:00-03:00"

API_CHECK_INTERVAL_DAYS = 30
TEAM_INACTIVITY_DAYS = 547
LICHESS_API_PAUSE = 1.1

os.makedirs(DATA_DIR_TORNEIOS, exist_ok=True)
os.makedirs(DATA_DIR_PLAYERS, exist_ok=True)

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

# --- FUNÇÕES AUXILIARES DE ARQUIVOS ---

def carregar_json(filepath, default_value):
    if not os.path.exists(filepath):
        return default_value
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        print(f"⚠ Aviso: Arquivo {filepath} não encontrado ou corrompido. Usando valor padrão.")
        return default_value

def salvar_json(filepath, data):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def converter_data_para_iso(data_valor):
    """Converte o valor 'startsAt' (ms ou string) para string ISO UTC."""
    if data_valor is None:
        return None
    
    if isinstance(data_valor, (int, float)):
        try:
            dt = datetime.fromtimestamp(data_valor / 1000, tz=timezone.utc)
            return dt.isoformat()
        except Exception as e:
            return None
    
    if isinstance(data_valor, str):
        try:
            dt = datetime.fromisoformat(data_valor.replace('Z', '+00:00'))
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt.isoformat()
        except Exception as e:
            return None
    return None

# --- NOVA FUNÇÃO: EXTRAÇÃO DE JOGADORES DAS PARTIDAS ---

def extrair_jogadores_dos_games(games_file_path):
    """Lê o ndjson de jogos e retorna um SET com os usernames únicos que jogaram."""
    players_in_games = set()
    if not os.path.exists(games_file_path):
        return players_in_games

    try:
        with open(games_file_path, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip(): continue
                try:
                    game = json.loads(line)
                    # Extrai White
                    white_user = game.get('players', {}).get('white', {}).get('user', {}).get('name')
                    if white_user: players_in_games.add(white_user)
                    
                    # Extrai Black
                    black_user = game.get('players', {}).get('black', {}).get('user', {}).get('name')
                    if black_user: players_in_games.add(black_user)
                except json.JSONDecodeError:
                    continue
    except Exception as e:
        print(f"⚠ Erro ao ler jogos em {games_file_path}: {e}")
    
    return players_in_games

# --- PARTE 1: ATUALIZAÇÃO DE TORNEIOS (CORE) ---

def get_existing_tournament_ids(directory):
    existing_ids = set()
    for filename in os.listdir(directory):
        if filename.endswith("_info.json"):
            existing_ids.add(filename.split("_")[0])
    return existing_ids

def fetch_all_team_tournaments(team_id):
    urls_to_fetch = [
        (f"https://lichess.org/api/team/{team_id}/arena", "arena"),
        (f"https://lichess.org/api/team/{team_id}/swiss", "swiss"),
    ]
    all_tournaments = []
    print("\n📡 Buscando lista de torneios da API do Lichess...")
    for url, tipo in urls_to_fetch:
        print(f"  -> Consultando {tipo}")
        try:
            resp = requests.get(url, stream=True)
            resp.raise_for_status()
            for line in resp.iter_lines():
                if not line: continue
                data = json.loads(line.decode("utf-8"))
                all_tournaments.append({
                    "id": data.get("id"),
                    "fullName": data.get("fullName", "Sem nome"),
                    "type": tipo,
                    "startsAt": data.get("startsAt")
                })
        except requests.exceptions.RequestException as e:
            print(f"⚠ Erro ao consultar API '{tipo}': {e}")
    print(f"✔ API retornou um total de {len(all_tournaments)} torneios.")
    return all_tournaments

def download_tournament_files(t_info, directory):
    tid = t_info["id"]
    tipo = t_info["type"]
    print(f"\n📥 Baixando detalhes para: {t_info.get('fullName', tid)} ({tid})")
    try:
        if tipo == "arena":
            base_url = f"https://lichess.org/api/tournament/{tid}"
        elif tipo == "swiss":
            base_url = f"https://lichess.org/api/swiss/{tid}"
        else:
            return None, None

        info_req = requests.get(base_url)
        info_req.raise_for_status()
        info_data = info_req.json()
        salvar_json(os.path.join(directory, f"{tid}_info.json"), info_data)
        
        results_req = requests.get(f"{base_url}/results", headers={"Accept": "application/x-ndjson"})
        results_req.raise_for_status()
        results_data = [json.loads(line) for line in results_req.text.strip().split('\n') if line]
        salvar_json(os.path.join(directory, f"{tid}_results.json"), results_data)

        games_req = requests.get(f"{base_url}/games", stream=True, headers={"Accept": "application/x-ndjson"})
        games_req.raise_for_status()
        with open(os.path.join(directory, f"{tid}_games.ndjson"), "w", encoding="utf-8") as f:
            for line in games_req.iter_lines():
                if line: f.write(line.decode('utf-8') + '\n')
        
        print(f"✔ Download de '{t_info.get('fullName', tid)}' concluído.")
        return info_data, results_data
    except Exception as e:
        print(f"!!! Erro ao baixar {tid}: {e}")
        return None, None

def _upsert_player(username, t_date_iso, t_date_dt, players_db, username_to_id_map, next_player_id):
    """Função auxiliar para criar ou atualizar jogador (reutilizada para ghosts e normais)"""
    player_id = username_to_id_map.get(username)

    if player_id is None:
        # Novo
        player_id = next_player_id
        new_player = {
            "id": player_id, "username": username,
            "first_seen_team_date": t_date_iso,
            "last_seen_team_date": t_date_iso,
            "last_seen_api_timestamp": None, "status": "active"
        }
        players_db.append(new_player)
        username_to_id_map[username] = player_id
    else:
        # Existente - Atualiza datas
        player_obj = next((p for p in players_db if p['id'] == player_id), None)
        if player_obj and t_date_dt:
            # First Seen
            current_first = player_obj.get("first_seen_team_date")
            update_first = False
            if not current_first: update_first = True
            else:
                try:
                    if t_date_dt < datetime.fromisoformat(current_first.replace('Z', '+00:00')): update_first = True
                except: update_first = True
            if update_first: player_obj["first_seen_team_date"] = t_date_iso

            # Last Seen
            current_last = player_obj.get("last_seen_team_date")
            update_last = False
            if not current_last: update_last = True
            else:
                try:
                    if t_date_dt > datetime.fromisoformat(current_last.replace('Z', '+00:00')): update_last = True
                except: update_last = True
            if update_last: player_obj["last_seen_team_date"] = t_date_iso
            
    return player_id

def update_player_databases(t_id, t_date_ms, results_data, players_db, username_to_id_map, participants_map, games_file_path=None, check_ghosts=False):
    """
    Atualiza players.json. 
    Se check_ghosts=True, compara quem jogou (games) com quem classificou (results)
    para encontrar jogadores removidos (possíveis trapaceiros/banidos).
    """
    if not results_data and not check_ghosts:
        return

    t_date_iso = converter_data_para_iso(t_date_ms)
    t_date_dt = None
    if t_date_iso:
        try:
            t_date_dt = datetime.fromisoformat(t_date_iso.replace('Z', '+00:00'))
        except ValueError: pass

    participant_ids = []
    # Determina o próximo ID livre
    if players_db:
        next_player_id = max([p['id'] for p in players_db]) + 1
    else:
        next_player_id = 1
    
    results_usernames = set()

    # 1. PROCESSA RESULTADOS OFICIAIS
    for entry in results_data:
        username = entry.get("username")
        if not username: continue
        results_usernames.add(username)
        
        player_id = _upsert_player(username, t_date_iso, t_date_dt, players_db, username_to_id_map, next_player_id)
        if player_id == next_player_id: next_player_id += 1
        participant_ids.append(player_id)

    # 2. PROCESSA FANTASMAS (CHECK_GHOSTS)
    if check_ghosts and games_file_path:
        print(f"  -> 👻 Investigando jogadores fantasmas (removidos)...")
        games_usernames = extrair_jogadores_dos_games(games_file_path)
        
        # Quem jogou MAS não está no resultado
        ghost_usernames = games_usernames - results_usernames
        
        if ghost_usernames:
            print(f"  -> ⚠ Encontrados {len(ghost_usernames)} fantasmas: {', '.join(list(ghost_usernames)[:5])}...")
            for ghost_user in ghost_usernames:
                # Adiciona o fantasma ao DB. Não marca como banned ainda (API fará isso).
                p_id = _upsert_player(ghost_user, t_date_iso, t_date_dt, players_db, username_to_id_map, next_player_id)
                if p_id == next_player_id: next_player_id += 1
                participant_ids.append(p_id)
        else:
            print("  -> Nenhum fantasma encontrado.")

    participants_map[t_id] = list(set(participant_ids))
    print(f"  -> Mapa de jogadores atualizado para {t_id}.")

def run_tournament_update():
    """Executa a Parte 1. Retorna True se houver mudanças, False se não."""
    print("--- INICIANDO PARTE 1: ATUALIZAÇÃO DE TORNEIOS ---")
    
    players_db = carregar_json(PLAYER_DB_FILE, [])
    participants_map = carregar_json(PARTICIPANTS_MAP_FILE, {})
    username_to_id_map = {p['username']: p['id'] for p in players_db}
    
    # Prepara data de corte
    metadata = carregar_json(STATUS_METADATA_FILE, {})
    ghost_cutoff_str = metadata.get("ghost_check_cutoff", DEFAULT_GHOST_CHECK_CUTOFF)
    try:
        ghost_cutoff_dt = datetime.fromisoformat(ghost_cutoff_str.replace('Z', '+00:00'))
    except:
        ghost_cutoff_dt = datetime.fromisoformat(DEFAULT_GHOST_CHECK_CUTOFF.replace('Z', '+00:00'))

    print(f"📅 Data de corte para verificação de fantasmas: {ghost_cutoff_dt.isoformat()}")
    
    existing_ids = get_existing_tournament_ids(DATA_DIR_TORNEIOS)
    all_lichess_tournaments = fetch_all_team_tournaments(TEAM_ID)
    
    new_tournaments = [t for t in all_lichess_tournaments if t["id"] not in existing_ids]
    unmapped_tournaments = [
        t for t in all_lichess_tournaments 
        if t["id"] in existing_ids and t["id"] not in participants_map
    ]

    tournaments_to_process = new_tournaments + unmapped_tournaments
    if not tournaments_to_process:
        print("\n✅ Nenhum torneio novo ou não mapeado para processar.")
        print("--- PARTE 1 CONCLUÍDA ---")
        return False

    print(f"\n✨ {len(new_tournaments)} novos torneios para baixar.")
    print(f"✨ {len(unmapped_tournaments)} torneios existentes para mapear.")
    
    changes_made = False
    for t_info in tournaments_to_process:
        tid = t_info["id"]
        
        if tid in new_tournaments:
            info_data, results_data = download_tournament_files(t_info, DATA_DIR_TORNEIOS)
        else:
            print(f"\n🔄 Processando torneio não mapeado: {tid}")
            info_data = carregar_json(os.path.join(DATA_DIR_TORNEIOS, f"{tid}_info.json"), None)
            results_data = carregar_json(os.path.join(DATA_DIR_TORNEIOS, f"{tid}_results.json"), None)
        
        if info_data and results_data:
            t_date_ms = info_data.get("startsAt")
            
            # --- LÓGICA DE DATA PARA FANTASMAS ---
            should_check_ghosts = False
            t_date_iso = converter_data_para_iso(t_date_ms)
            if t_date_iso:
                try:
                    t_dt = datetime.fromisoformat(t_date_iso.replace('Z', '+00:00'))
                    if t_dt >= ghost_cutoff_dt:
                        should_check_ghosts = True
                except: pass
            
            games_path = os.path.join(DATA_DIR_TORNEIOS, f"{tid}_games.ndjson")
            
            update_player_databases(tid, t_date_ms, results_data, players_db, username_to_id_map, participants_map, games_file_path=games_path, check_ghosts=should_check_ghosts)
            changes_made = True
        else:
            print(f"!!! Falha ao processar {tid}. Pulando.")
    
    if changes_made:
        print(f"\n💾 Salvando {len(players_db)} jogadores em '{PLAYER_DB_FILE}'...")
        salvar_json(PLAYER_DB_FILE, players_db)
        print(f"💾 Salvando {len(participants_map)} mapas de torneio em '{PARTICIPANTS_MAP_FILE}'...")
        salvar_json(PARTICIPANTS_MAP_FILE, participants_map)
        
        # Salva o cutoff usado se não existir
        if "ghost_check_cutoff" not in metadata:
            metadata["ghost_check_cutoff"] = DEFAULT_GHOST_CHECK_CUTOFF
            salvar_json(STATUS_METADATA_FILE, metadata)
    
    print("--- PARTE 1 CONCLUÍDA ---")
    return changes_made

# --- PARTE 2: ATUALIZAÇÃO DE STATUS DA API (CONDICIONAL) ---

def check_api_timer():
    """Verifica o timer. Retorna True se o timer expirou, False se não."""
    print("--- CHECANDO TIMER DA API (PARTE 2) ---")
    now = datetime.now(timezone.utc)
    metadata = carregar_json(STATUS_METADATA_FILE, {"last_api_check": None})
    last_check_str = metadata.get("last_api_check")
    
    if last_check_str:
        try:
            last_check_dt = datetime.fromisoformat(last_check_str)
            days_since_last_check = (now - last_check_dt).days
            if days_since_last_check < API_CHECK_INTERVAL_DAYS:
                print(f"✅ Checagem de API realizada há {days_since_last_check} dias. Timer não expirado.")
                return False 
            else:
                print(f"🗓️ Timer expirado! Última checagem há {days_since_last_check} dias.")
                return True 
        except ValueError:
            print("⚠ Data de última checagem inválida. Disparando checagem...")
            return True 
    else:
        print("ℹ️ Nenhuma checagem anterior registrada. Disparando checagem...")
        return True 

def run_api_status_check():
    """Executa a Parte 2: Checa API do Lichess para status."""
    print("\n--- INICIANDO PARTE 2: CHECAGEM DE STATUS DA API ---")
    print(f"⏳ Iniciando varredura da API...")

    players_db = carregar_json(PLAYER_DB_FILE, [])
    if not players_db:
        print("⚠ Nenhum jogador no banco de dados para checar. Pulando.")
        print("--- PARTE 2 CONCLUÍDA ---")
        return

    new_banned_list = []
    new_inactive_list = []
    today_dt = datetime.now(tz=timezone.utc)
    inactivity_threshold = timedelta(days=TEAM_INACTIVITY_DAYS)
    total_players = len(players_db)
    api_call_count = 0
    start_time = time.time()

    for i, player in enumerate(players_db):
        username = player["username"]
        original_status = player.get("status", "active") 
        player_updated = False 

        print(f"  -> Checando jogador {i+1}/{total_players}: {username} (Status atual: {original_status})", end="")

        if original_status != "banned":
            try:
                print(" (API...)", end="")
                api_call_count += 1
                response = requests.get(f"https://lichess.org/api/user/{username}")

                if response.status_code == 200:
                    api_data = response.json()
                    player["last_seen_api_timestamp"] = api_data.get("seenAt")

                    if api_data.get("tosViolation"):
                        if original_status != "banned":
                            player["status"] = "banned"
                            print(" -> BANIDO (ToS Violation)")
                            player_updated = True
                    elif api_data.get("disabled"):
                        if original_status != "closed":
                            player["status"] = "closed"
                            print(" -> CONTA FECHADA")
                            player_updated = True
                    elif original_status == "closed":
                         player["status"] = "active" 
                         print(" -> CONTA REABERTA!")
                         player_updated = True

                elif response.status_code == 404:
                    if original_status != "closed":
                        player["status"] = "closed"
                        print(" -> 404 (CONTA INEXISTENTE/FECHADA)")
                        player_updated = True
                else:
                    print(f" -> ERRO API ({response.status_code}). Mantendo status.")
                time.sleep(LICHESS_API_PAUSE)

            except Exception as e:
                print(f" -> ERRO INESPERADO: {e}. Mantendo status.")
                time.sleep(LICHESS_API_PAUSE)
        else:
            print(" (skip API: já banido)")

        # Checagem de Inatividade (Equipe)
        if player.get("status") not in ["banned", "closed"]:
            last_seen_team_str = player.get("last_seen_team_date")
            if last_seen_team_str:
                try:
                    last_seen_team_dt = datetime.fromisoformat(last_seen_team_str.replace('Z', '+00:00'))
                    if (today_dt - last_seen_team_dt) > inactivity_threshold:
                        if original_status != "inactive":
                           player["status"] = "inactive"
                           print(" -> INATIVO (Equipe)")
                           player_updated = True
                    else:
                        if original_status == "inactive": 
                            player["status"] = "active"
                            print(" -> REATIVADO (Equipe)")
                            player_updated = True
                        elif original_status == "closed":
                            player["status"] = "active"
                            print(" -> REATIVADO (Equipe)") 
                            player_updated = True
                except ValueError:
                    if original_status != "active":
                        player["status"] = "active"
                        player_updated = True
            else:
                 if original_status != "active":
                    player["status"] = "active"
                    player_updated = True

        if not player_updated and original_status != "banned":
             print(" (ok)")

        final_status = player.get("status", "active")
        if final_status == "banned":
            new_banned_list.append(username)
        elif final_status == "inactive":
            new_inactive_list.append(username)

    end_time = time.time()
    duration_minutes = (end_time - start_time) / 60
    print(f"\n📊 Varredura de API concluída em {duration_minutes:.2f} minutos ({api_call_count} chamadas).")

    print("\n💾 Salvando banco de dados de jogadores com status atualizado...")
    salvar_json(PLAYER_DB_FILE, players_db)
    print("💾 Salvando lista de acesso rápido de banidos...")
    salvar_json(BANNED_PLAYERS_FILE, new_banned_list)
    print("💾 Salvando lista de acesso rápido de inativos...")
    salvar_json(INACTIVE_PLAYERS_FILE, new_inactive_list)
    print("💾 Atualizando data da última checagem de API...")
    salvar_json(STATUS_METADATA_FILE, {"last_api_check": datetime.now(timezone.utc).isoformat()})
    print("--- PARTE 2 CONCLUÍDA ---")

if __name__ == "__main__":
    houve_mudancas = run_tournament_update()
    timer_expirou = check_api_timer()
    
    if houve_mudancas or timer_expirou:
        run_api_status_check()
    else:
        print("\n✅ Nenhum gatilho ativado. Pulando checagem de API (Parte 2).")

    print("\n🏁 Script finalizado.")