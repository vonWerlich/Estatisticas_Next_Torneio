# update_tournaments.py
import berserk
import os
import requests
import pandas as pd

# --- CONFIGURAÇÃO ---
TEAM_ID = "equipe-next"
DATA_DIR = "torneiosnew"
MAX_TOURNAMENTS = 100

os.makedirs(DATA_DIR, exist_ok=True)

# --- FUNÇÕES AUXILIARES ---

def get_existing_ids(directory):
    """Verifica o diretório e retorna um conjunto de IDs de torneios já baixados."""
    existing_ids = set()
    for filename in os.listdir(directory):
        if filename.endswith("_info.json"):
            tournament_id = filename.split("_")[0]
            existing_ids.add(tournament_id)
    print(f"Encontrados {len(existing_ids)} torneios existentes na pasta '{directory}'.")
    return existing_ids

def fetch_recent_tournaments(team_id, max_count):
    """Busca os torneios mais recentes de uma equipe via API (anônima)."""
    print(f"Buscando os {max_count} torneios mais recentes da equipe '{team_id}'...")
    try:
        session = berserk.Session() # Conexão anônima
        client = berserk.Client(session=session)
        recent_tournaments = client.teams.get_team_arenas(team_id, max=max_count)
        print(f"API do Lichess retornou {len(recent_tournaments)} torneios.")
        return recent_tournaments
    except Exception as e:
        print(f"Erro ao buscar torneios da API do Lichess: {e}")
        return []

def download_tournament_details(tournament_id, directory):
    """Baixa info, results e games de um único torneio."""
    print(f"Baixando detalhes para o novo torneio: {tournament_id}...")
    try:
        # Baixar info
        info_req = requests.get(f"https://lichess.org/api/tournament/{tournament_id}")
        info_req.raise_for_status()
        with open(os.path.join(directory, f"{tournament_id}_info.json"), "w", encoding="utf-8") as f:
            f.write(info_req.text)

        # Baixar results
        results_req = requests.get(f"https://lichess.org/api/tournament/{tournament_id}/results")
        results_req.raise_for_status()
        with open(os.path.join(directory, f"{tournament_id}_results.json"), "w", encoding="utf-8") as f:
            f.write(results_req.text)

        # Baixar games
        games_req = requests.get(f"https://lichess.org/api/tournament/{tournament_id}/games", stream=True)
        games_req.raise_for_status()
        with open(os.path.join(directory, f"{tournament_id}_games.ndjson"), "w", encoding="utf-8") as f:
            for line in games_req.iter_lines():
                if line:
                    f.write(line.decode('utf-8') + '\n')
        
        print(f"Detalhes de {tournament_id} baixados com sucesso.")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Erro ao baixar detalhes para {tournament_id}: {e}")
        return False

# --- FLUXO PRINCIPAL ---
if __name__ == "__main__":
    existing_tournament_ids = get_existing_ids(DATA_DIR)
    latest_tournaments = fetch_recent_tournaments(TEAM_ID, MAX_TOURNAMENTS)
    latest_tournament_ids = {t['id'] for t in latest_tournaments}
    new_tournament_ids = latest_tournament_ids - existing_tournament_ids

    if not new_tournament_ids:
        print("\nNenhum torneio novo para baixar. O diretório já está atualizado.")
    else:
        print(f"\nEncontrados {len(new_tournament_ids)} novos torneios para baixar: {', '.join(new_tournament_ids)}")
        success_count = 0
        for tid in new_tournament_ids:
            if download_tournament_details(tid, DATA_DIR):
                success_count += 1
        print(f"\nProcesso concluído. Baixados com sucesso: {success_count}/{len(new_tournament_ids)} novos torneios.")