import os
import json
import hashlib
import pathlib
import shutil
import time
from datetime import datetime

import duckdb
import chess
import pandas as pd
from huggingface_hub import HfApi, hf_hub_download
from huggingface_hub.utils import EntryNotFoundError

# ==============================================================================
# CONFIGURAÇÕES GERAIS
# ==============================================================================

DATASET_REPO = "vonWerlich/NEXT_Xadrez_Lichess_tournaments"
BASE_DIR = pathlib.Path("torneiosnew")
TEMP_DIR = pathlib.Path("temp_processing")

# Limite de segurança para evitar Timeouts em uploads gigantes
# Quando o backlog zerar, isso não fará diferença (pois haverá poucos novos).
MAX_TOURNAMENTS_PER_RUN = 50 

MANIFEST_PATH = pathlib.Path("processed_tournaments.json")

# Token precisa estar nas variáveis de ambiente
HF_TOKEN = os.getenv("HF_TOKEN_LICHESS")
if not HF_TOKEN:
    raise RuntimeError("Erro: A variável de ambiente HF_TOKEN_LICHESS não está definida.")

api = HfApi(token=HF_TOKEN)

# Inicializa o DuckDB em memória
con = duckdb.connect(database=':memory:')

# Cria estrutura base do DuckDB para acumular posições globais
con.execute("""
    CREATE TABLE global_new_positions (
        fen_hash VARCHAR,
        fen_str VARCHAR
    );
""")

# ==============================================================================
# FUNÇÕES UTILITÁRIAS
# ==============================================================================

def get_fen_hash(fen: str) -> str:
    return hashlib.sha1(fen.encode('utf-8')).hexdigest()

def canonical_fen(board: chess.Board) -> str:
    return " ".join(board.fen().split(" ")[:4])

def load_manifest():
    try:
        print("Baixando manifesto...")
        hf_hub_download(
            repo_id=DATASET_REPO,
            repo_type="dataset",
            filename="meta/processed_tournaments.json",
            local_dir="."
        )
        with open("meta/processed_tournaments.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        print("Manifesto não encontrado ou erro no download. Criando novo.")
        return {"tournaments": []}

# ==============================================================================
# PROCESSAMENTO LOCAL
# ==============================================================================

def process_tournament_file(ndjson_path: pathlib.Path, temp_games_dir, temp_moves_dir):
    tournament_id = ndjson_path.stem.replace("_games", "")
    
    games_buffer = []
    moves_buffer = []
    local_fens = {}

    with open(ndjson_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                game = json.loads(line)
            except:
                continue
            
            g_id = game.get('id')
            if not g_id: continue

            # 1. Metadados
            players = game.get('players', {})
            white = players.get('white', {})
            black = players.get('black', {})
            
            games_buffer.append({
                'game_id': g_id,
                'white': white.get('user', {}).get('name', 'Anonymous'),
                'black': black.get('user', {}).get('name', 'Anonymous'),
                'white_elo': white.get('rating', None),
                'black_elo': black.get('rating', None),
                'result': game.get('winner', 'draw'),
                'date': game.get('createdAt', 0),
                'tournament_id': tournament_id
            })

            # 2. Lances
            moves_str = game.get('moves', '')
            if not moves_str: continue
            
            board = chess.Board()
            moves = moves_str.split()
            ply = 0
            
            start_fen = canonical_fen(board)
            start_hash = get_fen_hash(start_fen)
            local_fens[start_hash] = start_fen
            
            for san in moves:
                try:
                    board.push_san(san)
                except:
                    break 
                
                ply += 1
                current_fen = canonical_fen(board)
                current_hash = get_fen_hash(current_fen)
                
                local_fens[current_hash] = current_fen
                
                moves_buffer.append({
                    'fen_hash': current_hash,
                    'game_id': g_id,
                    'ply': ply,
                    'move_san': san
                })

    if not games_buffer:
        return False

    # Salva GAMES localmente
    df_games = pd.DataFrame(games_buffer)
    con.execute("CREATE OR REPLACE TABLE temp_games AS SELECT * FROM df_games")
    games_out = temp_games_dir / f"{tournament_id}.parquet"
    con.execute(f"COPY temp_games TO '{games_out}' (FORMAT 'parquet')")

    # Salva MOVES localmente
    df_moves = pd.DataFrame(moves_buffer)
    con.execute("CREATE OR REPLACE TABLE temp_moves AS SELECT * FROM df_moves")
    moves_out = temp_moves_dir / f"{tournament_id}.parquet"
    con.execute(f"COPY temp_moves TO '{moves_out}' (FORMAT 'parquet', CODEC 'ZSTD')")

    # Acumula Posições
    pos_list = [{'fen_hash': h, 'fen_str': f} for h, f in local_fens.items()]
    df_pos = pd.DataFrame(pos_list)
    con.execute("INSERT INTO global_new_positions SELECT * FROM df_pos")
    
    con.execute("DROP TABLE temp_games; DROP TABLE temp_moves;")
    return True

# ==============================================================================
# SHARDS
# ==============================================================================

def sync_sharded_positions(temp_positions_dir):
    print("Preparando shards de posições...")
    prefixes = con.execute("""
        SELECT DISTINCT substring(fen_hash, 1, 2) 
        FROM global_new_positions
    """).fetchall()
    
    prefixes = [row[0] for row in prefixes]
    total_shards = len(prefixes)
    print(f"Total de shards afetados: {total_shards}")

    for i, prefix in enumerate(prefixes):
        remote_path = f"positions/prefix={prefix}/data.parquet"
        local_shard_dir = temp_positions_dir / f"prefix={prefix}"
        local_shard_dir.mkdir(parents=True, exist_ok=True)
        local_shard_file = local_shard_dir / "data.parquet"

        con.execute(f"""
            CREATE OR REPLACE TABLE current_new_batch AS 
            SELECT DISTINCT fen_hash, fen_str 
            FROM global_new_positions 
            WHERE substring(fen_hash, 1, 2) = '{prefix}'
        """)

        try:
            hf_hub_download(
                repo_id=DATASET_REPO,
                filename=remote_path,
                local_dir=TEMP_DIR,
                #local_dir_use_symlinks=False    # deprecado
            )
            downloaded_file = TEMP_DIR / remote_path
            con.execute(f"CREATE OR REPLACE TABLE remote_shard AS SELECT * FROM read_parquet('{downloaded_file}')")
        except (EntryNotFoundError, Exception):
            con.execute("CREATE OR REPLACE TABLE remote_shard (fen_hash VARCHAR, fen_str VARCHAR)")

        con.execute(f"""
            COPY (
                SELECT DISTINCT fen_hash, fen_str FROM (
                    SELECT * FROM remote_shard
                    UNION ALL
                    SELECT * FROM current_new_batch
                )
            ) TO '{local_shard_file}' (FORMAT 'parquet', CODEC 'ZSTD')
        """)

# ==============================================================================
# MAIN
# ==============================================================================

def main():
    # 1. Preparação de Diretórios
    if TEMP_DIR.exists(): shutil.rmtree(TEMP_DIR)
    TEMP_DIR.mkdir(parents=True)
    
    TEMP_GAMES_DIR = TEMP_DIR / "games"
    TEMP_MOVES_DIR = TEMP_DIR / "moves"
    TEMP_POSITIONS_DIR = TEMP_DIR / "positions"
    TEMP_META_DIR = TEMP_DIR / "meta"
    
    TEMP_GAMES_DIR.mkdir(parents=True)
    TEMP_MOVES_DIR.mkdir(parents=True)
    TEMP_POSITIONS_DIR.mkdir(parents=True)
    TEMP_META_DIR.mkdir(parents=True)

    manifest = load_manifest()
    processed_set = set(manifest["tournaments"])
    newly_processed = []

    # 2. Identificação e Filtro (AQUI ESTÁ A MÁGICA DO LIMITE)
    all_files = list(BASE_DIR.glob("*_games.ndjson"))
    
    # Filtra apenas os pendentes
    pending_files = []
    for f in all_files:
        tid = f.stem.replace("_games", "")
        if tid not in processed_set:
            pending_files.append(f)
            
    print(f"Total de torneios pendentes: {len(pending_files)}")

    # Aplica o limite (Fatiamento)
    files_to_process = pending_files[:MAX_TOURNAMENTS_PER_RUN]
    
    if not files_to_process:
        print("Nenhum torneio novo.")
        return

    print(f"Processando lote de {len(files_to_process)} torneios (Limite de segurança: {MAX_TOURNAMENTS_PER_RUN})...")

    # 3. Processamento Local
    for ndjson_file in files_to_process:
        tid = ndjson_file.stem.replace("_games", "")
        if process_tournament_file(ndjson_file, TEMP_GAMES_DIR, TEMP_MOVES_DIR):
            newly_processed.append(tid)

    print(f"\nTorneios processados neste lote: {len(newly_processed)}. Preparando Shards...")
    sync_sharded_positions(TEMP_POSITIONS_DIR)

    # 4. Atualiza Manifesto LOCALMENTE
    manifest["tournaments"].extend(newly_processed)
    with open(TEMP_META_DIR / "processed_tournaments.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    # 5. UPLOAD PARCELADO (Batch de 4 Commits)
    print("\nIniciando Upload Parcelado...")
    
    if any(TEMP_GAMES_DIR.iterdir()):
        print("-> Subindo Games...")
        api.upload_folder(
            folder_path=str(TEMP_GAMES_DIR),
            path_in_repo="games",
            repo_id=DATASET_REPO,
            repo_type="dataset",
            commit_message=f"Batch: {len(newly_processed)} games"
        )

    if any(TEMP_MOVES_DIR.iterdir()):
        print("-> Subindo Moves...")
        api.upload_folder(
            folder_path=str(TEMP_MOVES_DIR),
            path_in_repo="moves",
            repo_id=DATASET_REPO,
            repo_type="dataset",
            commit_message=f"Batch: {len(newly_processed)} moves"
        )

    if any(TEMP_POSITIONS_DIR.iterdir()):
        print("-> Subindo Posições...")
        api.upload_folder(
            folder_path=str(TEMP_POSITIONS_DIR),
            path_in_repo="positions",
            repo_id=DATASET_REPO,
            repo_type="dataset",
            commit_message="Batch: positions shards"
        )

    print("-> Subindo Manifesto...")
    api.upload_file(
        path_or_fileobj=str(TEMP_META_DIR / "processed_tournaments.json"),
        path_in_repo="meta/processed_tournaments.json",
        repo_id=DATASET_REPO,
        repo_type="dataset",
        commit_message="Update manifest"
    )
    
    print("\nSucesso Total! Limpeza final...")
    shutil.rmtree(TEMP_DIR)

if __name__ == "__main__":
    main()