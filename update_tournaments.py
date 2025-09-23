import os
import requests
import json
import sys

# --- CONFIGURAÇÃO ---
# ID correto da equipe, conforme seu script que já funciona.
TEAM_ID = "next-nucleo-de-estudos-em-xadrez--tecnologias"
DATA_DIR = "torneiosteste"

# Garante que o diretório de dados exista.
os.makedirs(DATA_DIR, exist_ok=True)

# Garante a codificação correta para o output no terminal
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

# --- FUNÇÕES AUXILIARES ---

def get_existing_tournament_ids(directory):
    """
    Verifica o diretório e retorna um conjunto de IDs de torneios já baixados.
    Um torneio é considerado 'baixado' se o arquivo _info.json existir.
    """
    existing_ids = set()
    for filename in os.listdir(directory):
        if filename.endswith("_info.json"):
            tournament_id = filename.split("_")[0]
            existing_ids.add(tournament_id)
    print(f"🔎 Encontrados {len(existing_ids)} torneios existentes na pasta '{directory}'.")
    return existing_ids

def fetch_all_team_tournaments(team_id):
    """
    Busca TODOS os torneios (Arena e Swiss) de uma equipe.
    Esta função é a lógica do seu script 'obterListadeTorneiosNextviaAPI.py'.
    """
    urls_to_fetch = [
        (f"https://lichess.org/api/team/{team_id}/arena", "arena"),
        (f"https://lichess.org/api/team/{team_id}/swiss", "swiss"),
    ]
    
    all_tournaments = []
    print("\n📡 Buscando lista de torneios da API do Lichess...")

    for url, tipo in urls_to_fetch:
        print(f"  -> Consultando {tipo} em {url}")
        try:
            resp = requests.get(url, stream=True)
            resp.raise_for_status()

            for line in resp.iter_lines():
                if not line:
                    continue
                data = json.loads(line.decode("utf-8"))
                tournament_info = {
                    "id": data.get("id"),
                    "fullName": data.get("fullName", "Sem nome"),
                    "type": tipo
                }
                all_tournaments.append(tournament_info)
        except requests.exceptions.RequestException as e:
            print(f"⚠ Erro ao consultar a API para torneios do tipo '{tipo}': {e}")
            
    print(f"✔ API retornou um total de {len(all_tournaments)} torneios.")
    return all_tournaments

def download_tournament_files(tournament_info, directory):
    """
    Baixa os arquivos de info, results e games para um único torneio.
    Esta função combina a lógica do seu 'getTorneiosFromLichessAPIbyLinksinCSV.py'.
    """
    tid = tournament_info["id"]
    tipo = tournament_info["type"]
    
    print(f"\n📥 Baixando detalhes para o novo torneio: {tournament_info['fullName']} ({tid}) [{tipo}]")

    try:
        # Define as URLs baseadas no tipo de torneio
        if tipo == "arena":
            url_info = f"https://lichess.org/api/tournament/{tid}"
            url_results = f"https://lichess.org/api/tournament/{tid}/results"
            url_games = f"https://lichess.org/api/tournament/{tid}/games"
        elif tipo == "swiss":
            url_info = f"https://lichess.org/api/swiss/{tid}"
            url_results = f"https://lichess.org/api/swiss/{tid}/results"
            url_games = f"https://lichess.org/api/swiss/{tid}/games"
        else:
            print(f"!!! Tipo de torneio desconhecido: '{tipo}'. Ignorando.")
            return False

        # 1. Baixar Metadados (info)
        info_req = requests.get(url_info)
        info_req.raise_for_status()
        with open(os.path.join(directory, f"{tid}_info.json"), "w", encoding="utf-8") as f:
            json.dump(info_req.json(), f, ensure_ascii=False, indent=2)
        print(f"  -> Metadados salvos.")

        # 2. Baixar Resultados (results)
        results_req = requests.get(url_results, headers={"Accept": "application/x-ndjson"})
        results_req.raise_for_status()
        results_data = [json.loads(line) for line in results_req.text.strip().split('\n')]
        with open(os.path.join(directory, f"{tid}_results.json"), "w", encoding="utf-8") as f:
            json.dump(results_data, f, ensure_ascii=False, indent=2)
        print(f"  -> Resultados salvos.")

        # 3. Baixar Partidas (games)
        games_req = requests.get(url_games, stream=True, headers={"Accept": "application/x-ndjson"})
        games_req.raise_for_status()
        with open(os.path.join(directory, f"{tid}_games.ndjson"), "w", encoding="utf-8") as f:
            for line in games_req.iter_lines():
                if line:
                    f.write(line.decode('utf-8') + '\n')
        print(f"  -> Partidas salvas.")
        
        print(f"✔ Download de '{tournament_info['fullName']}' concluído.")
        return True

    except requests.exceptions.RequestException as e:
        print(f"!!! Erro ao baixar detalhes para o torneio {tid}: {e}")
        # Se houve um erro, limpa arquivos parcialmente baixados para este torneio
        for suffix in ["_info.json", "_results.json", "_games.ndjson"]:
            partial_file = os.path.join(directory, f"{tid}{suffix}")
            if os.path.exists(partial_file):
                os.remove(partial_file)
        return False

# --- FLUXO PRINCIPAL ---
if __name__ == "__main__":
    # 1. Obter a lista de IDs de torneios que já temos salvos localmente
    existing_ids = get_existing_tournament_ids(DATA_DIR)
    
    # 2. Buscar a lista COMPLETA e atual de todos os torneios (Arena e Swiss) da API
    all_lichess_tournaments = fetch_all_team_tournaments(TEAM_ID)
    
    # 3. Identificar quais torneios são novos
    new_tournaments = [
        t for t in all_lichess_tournaments if t["id"] not in existing_ids
    ]

    if not new_tournaments:
        print("\n✅ Nenhum torneio novo para baixar. O diretório já está atualizado.")
    else:
        print(f"\n✨ Encontrados {len(new_tournaments)} novos torneios para baixar.")
        success_count = 0
        for tournament in new_tournaments:
            if download_tournament_files(tournament, DATA_DIR):
                success_count += 1
                
        print(f"\n🏁 Processo concluído. Baixados com sucesso: {success_count}/{len(new_tournaments)} novos torneios.")