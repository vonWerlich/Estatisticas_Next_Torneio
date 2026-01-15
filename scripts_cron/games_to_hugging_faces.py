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

# Subpastas para organizar o Batch Upload
TEMP_GAMES_DIR = TEMP_DIR / "games"
TEMP_MOVES_DIR = TEMP_DIR / "moves"
TEMP_POSITIONS_DIR = TEMP_DIR / "positions"

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
# FUNÇÕES UTILITÁRIAS (XADREZ & HASH)
# ==============================================================================

def get_fen_hash(fen: str) -> str:
    return hashlib.sha1(fen.encode('utf-8')).hexdigest()

def canonical_fen(board: chess.Board) -> str:
    return " ".join(board.fen().split(" ")[:4])

# ==============================================================================
# GERENCIAMENTO DO MANIFESTO
# ==============================================================================

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

def save_manifest(manifest):
    os.makedirs("meta", exist_ok=True)
    with open("meta/processed_tournaments.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    
    # Upload final do manifesto
    api.upload_file(
        path_or_fileobj="meta/processed_tournaments.json",
        path_in_repo="meta/processed_tournaments.json",
        repo_id=DATASET_REPO,
        repo_type="dataset",
        commit_message="Update manifest"
    )

# ==============================================================================
# FASE 1: PROCESSAMENTO DE TORNEIOS (ETL - SAVE LOCAL)
# ==============================================================================

def process_tournament_file(ndjson_path: pathlib.Path):
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

            # --- 1. Metadados ---
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

            # --- 2. Lances ---
            moves_str = game.get('moves', '')
            if not moves_str: continue
            
            board = chess.Board()
            moves = moves_str.split()
            ply = 0
            
            # Posição inicial
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

    # A. Salvar GAMES localmente (SEM UPLOAD AGORA)
    df_games = pd.DataFrame(games_buffer)
    con.execute("CREATE OR REPLACE TABLE temp_games AS SELECT * FROM df_games")
    
    games_out = TEMP_GAMES_DIR / f"{tournament_id}.parquet"
    con.execute(f"COPY temp_games TO '{games_out}' (FORMAT 'parquet')")

    # B. Salvar MOVES localmente (SEM UPLOAD AGORA)
    df_moves = pd.DataFrame(moves_buffer)
    con.execute("CREATE OR REPLACE TABLE temp_moves AS SELECT * FROM df_moves")
    
    moves_out = TEMP_MOVES_DIR / f"{tournament_id}.parquet"
    con.execute(f"COPY temp_moves TO '{moves_out}' (FORMAT 'parquet', CODEC 'ZSTD')")

    # C. Acumular Posições na Memória
    pos_list = [{'fen_hash': h, 'fen_str': f} for h, f in local_fens.items()]
    df_pos = pd.DataFrame(pos_list)
    con.execute("INSERT INTO global_new_positions SELECT * FROM df_pos")
    
    # Limpeza DuckDB
    con.execute("DROP TABLE temp_games; DROP TABLE temp_moves;")
    
    return True

# ==============================================================================
# FASE 2: SHARDS (BATCH UPLOAD)
# ==============================================================================

def sync_sharded_positions():
    print("Preparando shards de posições...")
    prefixes = con.execute("""
        SELECT DISTINCT substring(fen_hash, 1, 2) 
        FROM global_new_positions
    """).fetchall()
    
    prefixes = [row[0] for row in prefixes]
    total_shards = len(prefixes)
    print(f"Total de shards afetados: {total_shards}")

    # Processa cada shard e salva localmente
    for i, prefix in enumerate(prefixes):
        remote_path = f"positions/prefix={prefix}/data.parquet"
        
        # Estrutura local precisa imitar a remota para o upload_folder funcionar bem
        # Local: temp_processing/positions/prefix=XY/data.parquet
        local_shard_dir = TEMP_POSITIONS_DIR / f"prefix={prefix}"
        local_shard_dir.mkdir(parents=True, exist_ok=True)
        local_shard_file = local_shard_dir / "data.parquet"

        # 1. Pega dados novos deste prefixo
        con.execute(f"""
            CREATE OR REPLACE TABLE current_new_batch AS 
            SELECT DISTINCT fen_hash, fen_str 
            FROM global_new_positions 
            WHERE substring(fen_hash, 1, 2) = '{prefix}'
        """)

        # 2. Baixa dados antigos (se existirem)
        temp_download_path = TEMP_DIR / f"download_{prefix}.parquet"
        try:
            hf_hub_download(
                repo_id=DATASET_REPO,
                filename=remote_path,
                local_dir=TEMP_DIR,
                local_dir_use_symlinks=False
            )
            # O arquivo baixa mantendo a estrutura de pastas em TEMP_DIR
            downloaded_file = TEMP_DIR / remote_path
            con.execute(f"CREATE OR REPLACE TABLE remote_shard AS SELECT * FROM read_parquet('{downloaded_file}')")
        except (EntryNotFoundError, Exception):
            # Se não existe ou deu erro no download, assumimos vazio
            con.execute("CREATE OR REPLACE TABLE remote_shard (fen_hash VARCHAR, fen_str VARCHAR)")

        # 3. Merge e Salva Localmente
        con.execute(f"""
            COPY (
                SELECT DISTINCT fen_hash, fen_str FROM (
                    SELECT * FROM remote_shard
                    UNION ALL
                    SELECT * FROM current_new_batch
                )
            ) TO '{local_shard_file}' (FORMAT 'parquet', CODEC 'ZSTD')
        """)
        
        # Opcional: imprimir progresso a cada 10 shards
        if i % 10 == 0:
            print(f"   Processado shard {prefix}...")

# ==============================================================================
# MAIN
# ==============================================================================

def main():
    # 1. Preparação de Diretórios
    if TEMP_DIR.exists(): shutil.rmtree(TEMP_DIR)
    TEMP_DIR.mkdir(parents=True)
    TEMP_GAMES_DIR.mkdir(parents=True)
    TEMP_MOVES_DIR.mkdir(parents=True)
    TEMP_POSITIONS_DIR.mkdir(parents=True)

    manifest = load_manifest()
    processed_set = set(manifest["tournaments"])
    newly_processed = []

    # 2. Processamento Local (Sem Uploads)
    found_files = list(BASE_DIR.glob("*_games.ndjson"))
    print(f"Encontrados {len(found_files)} arquivos. Processando...")

    for ndjson_file in found_files:
        tid = ndjson_file.stem.replace("_games", "")
        if tid in processed_set: continue
            
        if process_tournament_file(ndjson_file):
            newly_processed.append(tid)

    if not newly_processed:
        print("Nenhum torneio novo.")
        return

    print(f"\nTorneios processados: {len(newly_processed)}. Preparando Shards...")
    
    # 3. Preparação dos Shards (Sem Uploads ainda)
    sync_sharded_positions()

    # 4. FASE DE UPLOAD EM LOTE (AQUI É O PULO DO GATO)
    print("\nIniciando Upload em Lote (Isso economiza API calls)...")

    # A. Upload Games (1 Commit para todos os jogos novos)
    if any(TEMP_GAMES_DIR.iterdir()):
        print("Subindo pasta Games...")
        api.upload_folder(
            folder_path=str(TEMP_GAMES_DIR),
            path_in_repo="games",
            repo_id=DATASET_REPO,
            repo_type="dataset",
            commit_message=f"Batch upload: {len(newly_processed)} tournaments (games)"
        )

    # B. Upload Moves (1 Commit para todos os movimentos novos)
    if any(TEMP_MOVES_DIR.iterdir()):
        print("Subindo pasta Moves...")
        api.upload_folder(
            folder_path=str(TEMP_MOVES_DIR),
            path_in_repo="moves",
            repo_id=DATASET_REPO,
            repo_type="dataset",
            commit_message=f"Batch upload: {len(newly_processed)} tournaments (moves)"
        )

    # C. Upload Positions (1 Commit para todos os shards alterados)
    if any(TEMP_POSITIONS_DIR.iterdir()):
        print("Subindo Shards de Posições...")
        api.upload_folder(
            folder_path=str(TEMP_POSITIONS_DIR),
            path_in_repo="positions",
            repo_id=DATASET_REPO,
            repo_type="dataset",
            commit_message="Batch upload: position shards update"
        )

    # 5. Atualiza Manifesto
    manifest["tournaments"].extend(newly_processed)
    save_manifest(manifest)
    
    print("\nSucesso Total! Limpeza final...")
    shutil.rmtree(TEMP_DIR)

if __name__ == "__main__":
    main()