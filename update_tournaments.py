import os
import requests
import json
import sys
import time
from datetime import datetime, timedelta, timezone

# --- CONFIGURAÇÃO ---
# (Sem mudanças aqui, tudo igual)
TEAM_ID = "next-nucleo-de-estudos-em-xadrez--tecnologias"
DATA_DIR_TORNEIOS = "torneiosnew"
DATA_DIR_PLAYERS = "player_data"

PLAYER_DB_FILE = os.path.join(DATA_DIR_PLAYERS, "players.json")
PARTICIPANTS_MAP_FILE = os.path.join(DATA_DIR_PLAYERS, "tournament_participants.json")
BANNED_PLAYERS_FILE = os.path.join(DATA_DIR_PLAYERS, "banned_players.json")
INACTIVE_PLAYERS_FILE = os.path.join(DATA_DIR_PLAYERS, "inactive_players.json")
STATUS_METADATA_FILE = os.path.join(DATA_DIR_PLAYERS, "status_metadata.json")

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
    
    # Caso 1: É um timestamp (int ou float)
    if isinstance(data_valor, (int, float)):
        try:
            dt = datetime.fromtimestamp(data_valor / 1000, tz=timezone.utc)
            return dt.isoformat()
        except Exception as e:
            print(f"  -> ⚠ Erro ao converter timestamp {data_valor}: {e}")
            return None
    
    # Caso 2: É uma string (formato ISO)
    if isinstance(data_valor, str):
        try:
            # Tenta converter a string para um objeto datetime
            dt = datetime.fromisoformat(data_valor.replace('Z', '+00:00'))
            
            # Se a string não tiver fuso horário, assume UTC
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            
            # Converte de volta para string ISO UTC padronizada
            return dt.isoformat()
        except Exception as e:
            print(f"  -> ⚠ Erro ao converter string de data {data_valor}: {e}")
            return None
    
    # Outros tipos
    return None

# --- PARTE 1: ATUALIZAÇÃO DE TORNEIOS (SEMPRE RODA) ---
# (Sem mudanças aqui, get_existing_tournament_ids, fetch_all_team_tournaments,
# download_tournament_files, update_player_databases)
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

def update_player_databases(t_id, t_date_ms, results_data, players_db, username_to_id_map, participants_map):
    """Atualiza o 'players.json' e 'participants_map.json' (em memória),
       garantindo a ordem cronológica correta para first_seen e last_seen."""
    if not results_data:
        return

    # Converte a data do torneio para objeto datetime (para comparação)
    t_date_dt = None
    t_date_iso = converter_data_para_iso(t_date_ms) # Usa a função corrigida
    if t_date_iso:
        try:
            # Converte a string ISO de volta para datetime para poder comparar
            t_date_dt = datetime.fromisoformat(t_date_iso.replace('Z', '+00:00'))
        except ValueError:
            print(f"  -> ⚠ Erro ao re-converter data ISO {t_date_iso} para datetime.")
            t_date_dt = None # Trata como se não tivesse data se a conversão falhar

    # Aviso se ainda assim não tiver data
    if t_date_dt is None:
        print(f"  -> ⚠ Aviso: Torneio {t_id} não tem data válida. 'Seen' dates não serão atualizadas.")

    participant_ids = []
    next_player_id = max([p['id'] for p in players_db] + [0]) + 1

    for entry in results_data:
        username = entry.get("username")
        if not username:
            continue

        player_id = username_to_id_map.get(username)

        if player_id is None:
            # --- Jogador Novo ---
            player_id = next_player_id
            new_player = {
                "id": player_id, "username": username,
                # Define ambas as datas inicialmente com a data deste torneio
                "first_seen_team_date": t_date_iso,
                "last_seen_team_date": t_date_iso,
                "last_seen_api_timestamp": None, "status": "active"
            }
            players_db.append(new_player)
            username_to_id_map[username] = player_id
            next_player_id += 1
        else:
            # --- Jogador Existente ---
            player_obj = next((p for p in players_db if p['id'] == player_id), None)
            if player_obj and t_date_dt: # Só atualiza se tivermos uma data válida para comparar

                # 1. Atualiza first_seen SE a data atual for MAIS ANTIGA
                current_first_seen_str = player_obj.get("first_seen_team_date")
                needs_first_seen_update = False
                if current_first_seen_str:
                    try:
                        current_first_seen_dt = datetime.fromisoformat(current_first_seen_str.replace('Z', '+00:00'))
                        if t_date_dt < current_first_seen_dt:
                            needs_first_seen_update = True
                    except ValueError:
                        needs_first_seen_update = True # Se a data antiga for inválida, atualiza
                else:
                    needs_first_seen_update = True # Se não tinha data antiga, atualiza

                if needs_first_seen_update:
                    player_obj["first_seen_team_date"] = t_date_iso

                # 2. Atualiza last_seen SE a data atual for MAIS NOVA
                current_last_seen_str = player_obj.get("last_seen_team_date")
                needs_last_seen_update = False
                if current_last_seen_str:
                    try:
                        current_last_seen_dt = datetime.fromisoformat(current_last_seen_str.replace('Z', '+00:00'))
                        if t_date_dt > current_last_seen_dt:
                            needs_last_seen_update = True
                    except ValueError:
                        needs_last_seen_update = True # Se a data antiga for inválida, atualiza
                else:
                    needs_last_seen_update = True # Se não tinha data antiga, atualiza

                if needs_last_seen_update:
                    player_obj["last_seen_team_date"] = t_date_iso

        participant_ids.append(player_id)

    participants_map[t_id] = list(set(participant_ids))
    print(f"  -> Mapa de jogadores atualizado para {t_id}.")

def run_tournament_update():
    """Executa a Parte 1. Retorna True se houver mudanças, False se não."""
    print("--- INICIANDO PARTE 1: ATUALIZAÇÃO DE TORNEIOS ---")
    
    players_db = carregar_json(PLAYER_DB_FILE, [])
    participants_map = carregar_json(PARTICIPANTS_MAP_FILE, {})
    username_to_id_map = {p['username']: p['id'] for p in players_db}
    
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
        return False # Retorna False se nada foi atualizado

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
            update_player_databases(tid, t_date_ms, results_data, players_db, username_to_id_map, participants_map)
            changes_made = True
        else:
            print(f"!!! Falha ao processar {tid}. Pulando.")
    
    if changes_made:
        print(f"\n💾 Salvando {len(players_db)} jogadores em '{PLAYER_DB_FILE}'...")
        salvar_json(PLAYER_DB_FILE, players_db)
        print(f"💾 Salvando {len(participants_map)} mapas de torneio em '{PARTICIPANTS_MAP_FILE}'...")
        salvar_json(PARTICIPANTS_MAP_FILE, participants_map)
    
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
                return False # Timer NÃO expirou
            else:
                print(f"🗓️ Timer expirado! Última checagem há {days_since_last_check} dias.")
                return True # Timer expirou
        except ValueError:
            print("⚠ Data de última checagem inválida. Disparando checagem...")
            return True # Força a checagem se a data for inválida
    else:
        print("ℹ️ Nenhuma checagem anterior registrada. Disparando checagem...")
        return True # Força a checagem se nunca rodou

def run_api_status_check():
    """
    Executa a Parte 2: Checa API do Lichess para status (banido/fechado/visto por último)
    e atualiza status de inatividade da equipe. Roda condicionalmente.
    """
    print("\n--- INICIANDO PARTE 2: CHECAGEM DE STATUS DA API ---")
    print(f"⏳ Iniciando varredura da API...")

    players_db = carregar_json(PLAYER_DB_FILE, [])
    if not players_db:
        print("⚠ Nenhum jogador no banco de dados para checar. Pulando.")
        print("--- PARTE 2 CONCLUÍDA ---")
        return

    # Carrega as listas atuais para referência, mas elas serão recriadas
    current_banned = set(carregar_json(BANNED_PLAYERS_FILE, []))
    current_inactive = set(carregar_json(INACTIVE_PLAYERS_FILE, []))

    new_banned_list = []
    new_inactive_list = []
    # Poderíamos ter uma new_closed_list, mas por ora, só o status no players.json basta.

    today_dt = datetime.now(tz=timezone.utc)
    inactivity_threshold = timedelta(days=TEAM_INACTIVITY_DAYS)

    total_players = len(players_db)
    api_call_count = 0
    start_time = time.time()

    for i, player in enumerate(players_db):
        username = player["username"]
        original_status = player.get("status", "active") # Pega status atual ou assume 'active'
        player_updated = False # Flag para saber se houve mudança

        print(f"  -> Checando jogador {i+1}/{total_players}: {username} (Status atual: {original_status})", end="")

        # --- Etapa 1: Checagem de API (Banido/Fechado/LastSeen) ---
        # Pula APENAS se já sabemos que está banido (tosViolation)
        # Contas fechadas ('closed') podem ser reabertas ou renomeadas (raro, mas possível),
        # então vale a pena checar de vez em quando.
        if original_status != "banned":
            try:
                print(" (API...)", end="")
                api_call_count += 1
                response = requests.get(f"https://lichess.org/api/user/{username}")

                if response.status_code == 200:
                    api_data = response.json()
                    player["last_seen_api_timestamp"] = api_data.get("seenAt")

                    # LÓGICA DE STATUS: Prioridade para Banido > Fechado
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
                    # Se não está banido nem fechado, ele está 'ok' na API.
                    # A inatividade será tratada na próxima etapa. Se ele estava 'closed' antes, volta a 'active'.
                    elif original_status == "closed":
                         player["status"] = "active" # Conta reaberta!
                         print(" -> CONTA REABERTA!")
                         player_updated = True

                elif response.status_code == 404:
                    # Se a conta não existe mais, consideramos como fechada permanentemente
                    if original_status != "closed":
                        player["status"] = "closed" # Ou 'banned' se preferir tratar 404 assim
                        print(" -> 404 (CONTA INEXISTENTE/FECHADA)")
                        player_updated = True
                else:
                    # Mantém o status original em caso de erro da API
                    print(f" -> ERRO API ({response.status_code}). Mantendo status.")

                # A PAUSA CRÍTICA
                time.sleep(LICHESS_API_PAUSE)

            except Exception as e:
                print(f" -> ERRO INESPERADO: {e}. Mantendo status.")
                # Pausa mesmo em erro para não bombardear a API
                time.sleep(LICHESS_API_PAUSE)
        else:
            print(" (skip API: já banido)")

        # --- Etapa 2: Checagem de Inatividade (Equipe) ---
        # Só executa se o jogador NÃO estiver banido ou fechado pela API
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
                        if original_status == "inactive": # Se estava inativo e voltou
                            player["status"] = "active"
                            print(" -> REATIVADO (Equipe)")
                            player_updated = True
                        elif original_status == "closed": # Se estava fechado e jogou
                            player["status"] = "active"
                            print(" -> REATIVADO (Equipe, estava fechado?)") # Log estranho
                            player_updated = True
                        # Se já estava 'active', não precisa mudar
                except ValueError:
                    # Se a data for inválida, não podemos determinar inatividade, assume active
                    if original_status != "active":
                        player["status"] = "active"
                        player_updated = True
            else:
                 # Se nunca foi visto em torneio com data, assume active
                 if original_status != "active":
                    player["status"] = "active"
                    player_updated = True

        # Se não houve mudança de status detectada, imprime (ok)
        if not player_updated and original_status != "banned":
             print(" (ok)")

        # --- Etapa 3: Atualiza as listas de acesso rápido ---
        final_status = player.get("status", "active")
        if final_status == "banned":
            new_banned_list.append(username)
        elif final_status == "inactive":
            new_inactive_list.append(username)
        # Não precisamos de uma lista rápida para 'closed', a menos que você queira

    # --- Etapa 4: Salvar tudo ---
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


# --- FLUXO PRINCIPAL ---
if __name__ == "__main__":
    
    # Executa a Parte 1 e armazena se ela fez alguma mudança
    houve_mudancas_nos_torneios = run_tournament_update()
    
    # Executa a checagem do timer
    timer_da_api_expirou = check_api_timer()
    
    # A LÓGICA DO "OU" QUE VOCÊ PEDIU:
    if houve_mudancas_nos_torneios or timer_da_api_expirou:
        if houve_mudancas_nos_torneios:
            print("\n>> GATILHO: Novos torneios foram processados.")
        if timer_da_api_expirou:
            print("\n>> GATILHO: Timer de 30 dias da API expirou.")
            
        # Executa a Parte 2 (o trabalho caro)
        run_api_status_check()
    else:
        print("\n✅ Nenhum gatilho ativado. Pulando checagem de API (Parte 2).")

    print("\n🏁 Script finalizado.")