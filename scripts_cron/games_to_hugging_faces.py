import os
import json
import hashlib
import pathlib
import shutil
import time
from datetime import datetime

import duckdb
import chess
from huggingface_hub import HfApi, hf_hub_download
from huggingface_hub.utils import EntryNotFoundError

# ==============================================================================
# CONFIGURAÇÕES GERAIS
# ==============================================================================

DATASET_REPO = "vonWerlich/NEXT_Xadrez_Lichess_tournaments"
BASE_DIR = pathlib.Path("torneiosnew")
TEMP_DIR = pathlib.Path("temp_processing")
MANIFEST_PATH = pathlib.Path("processed_tournaments.json")

# Token precisa estar nas variáveis de ambiente ou colado aqui (não recomendado)
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
    """Gera o SHA1 da string FEN."""
    return hashlib.sha1(fen.encode('utf-8')).hexdigest()

def canonical_fen(board: chess.Board) -> str:
    """Retorna o FEN simplificado (apenas peças, vez, roque e en passant)."""
    # Exemplo: rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -
    return " ".join(board.fen().split(" ")[:4])

# ==============================================================================
# GERENCIAMENTO DO MANIFESTO (CONTROLE DE ESTADO)
# ==============================================================================

def load_manifest():
    """Baixa a lista de torneios já processados."""
    try:
        print("Baixando manifesto...")
        hf_hub_download(
            repo_id=DATASET_REPO,
            repo_type="dataset",
            filename="meta/processed_tournaments.json",
            local_dir=".",
            local_dir_use_symlinks=False
        )
        with open("meta/processed_tournaments.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        print("Manifesto não encontrado ou erro no download. Criando novo.")
        return {"tournaments": []}

def save_manifest(manifest):
    """Salva e sobe a lista atualizada."""
    os.makedirs("meta", exist_ok=True)
    with open("meta/processed_tournaments.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    
    api.upload_file(
        path_or_fileobj="meta/processed_tournaments.json",
        path_in_repo="meta/processed_tournaments.json",
        repo_id=DATASET_REPO,
        repo_type="dataset"
    )

# ==============================================================================
# FASE 1: PROCESSAMENTO DE TORNEIOS (ETL)
# ==============================================================================

def process_tournament_file(ndjson_path: pathlib.Path):
    """Lê um arquivo NDJSON, extrai dados e popula o DuckDB."""
    tournament_id = ndjson_path.stem.replace("_games", "")
    
    games_buffer = []
    moves_buffer = []
    local_fens = {} # Dict para dedup rápida dentro do torneio

    with open(ndjson_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                game = json.loads(line)
            except:
                continue
            
            g_id = game.get('id')
            if not g_id: continue

            # --- 1. Dados do Jogo (Metadata) ---
            players = game.get('players', {})
            white = players.get('white', {})
            black = players.get('black', {})
            
            games_buffer.append({
                'game_id': g_id,
                'white': white.get('user', {}).get('name', 'Anonymous'),
                'black': black.get('user', {}).get('name', 'Anonymous'),
                'white_elo': white.get('rating', None),
                'black_elo': black.get('rating', None),
                'result': game.get('winner', 'draw'), # 'white', 'black', or 'draw' (check lichess api specificities)
                'date': game.get('createdAt', 0),
                'tournament_id': tournament_id
            })

            # --- 2. Dados dos Movimentos (Lances) ---
            moves_str = game.get('moves', '')
            if not moves_str: continue
            
            board = chess.Board()
            moves = moves_str.split()
            ply = 0
            
            # Adiciona a posição inicial também? Geralmente sim.
            start_fen = canonical_fen(board)
            start_hash = get_fen_hash(start_fen)
            local_fens[start_hash] = start_fen
            
            # Registra o estado INICIAL (Ply 0) se quiser rastrear tabuleiros,
            # mas geralmente rastreamos o movimento QUE LEVOU à posição. 
            # Neste modelo 'moves', vamos salvar: 
            # "Neste jogo, no ply X, foi jogado 'e4', resultando no hash Y"
            
            for san in moves:
                try:
                    board.push_san(san)
                except:
                    break # Lance inválido, para o processamento deste jogo
                
                ply += 1
                current_fen = canonical_fen(board)
                current_hash = get_fen_hash(current_fen)
                
                # Guarda no buffer de posições únicas
                local_fens[current_hash] = current_fen
                
                # Guarda o lance
                moves_buffer.append({
                    'fen_hash': current_hash,
                    'game_id': g_id,
                    'ply': ply,
                    'move_san': san
                })

    # --- 3. Inserção e Upload (Por Torneio) ---
    if not games_buffer:
        return False

    # A. Salvar/Upload GAMES
    con.execute("CREATE OR REPLACE TABLE temp_games AS SELECT * FROM games_buffer_df", {"games_buffer_df": games_buffer})
    
    games_out = TEMP_DIR / f"games_{tournament_id}.parquet"
    con.execute(f"COPY temp_games TO '{games_out}' (FORMAT 'parquet')")
    
    api.upload_file(
        path_or_fileobj=str(games_out),
        path_in_repo=f"games/{tournament_id}.parquet",
        repo_id=DATASET_REPO,
        repo_type="dataset"
    )

    # B. Salvar/Upload MOVES (Compressão ZSTD recomendada para texto repetitivo)
    con.execute("CREATE OR REPLACE TABLE temp_moves AS SELECT * FROM moves_buffer_df", {"moves_buffer_df": moves_buffer})
    
    moves_out = TEMP_DIR / f"moves_{tournament_id}.parquet"
    con.execute(f"COPY temp_moves TO '{moves_out}' (FORMAT 'parquet', CODEC 'ZSTD')")
    
    api.upload_file(
        path_or_fileobj=str(moves_out),
        path_in_repo=f"moves/{tournament_id}.parquet",
        repo_id=DATASET_REPO,
        repo_type="dataset"
    )

    # C. Acumular Posições na Tabela Global (Para Sharding depois)
    # Transforma dict em lista de tuplas para inserção
    pos_list = [{'fen_hash': h, 'fen_str': f} for h, f in local_fens.items()]
    
    # Inserimos na tabela global. O DISTINCT será feito na hora do sync.
    con.execute("INSERT INTO global_new_positions SELECT * FROM pos_list_df", {"pos_list_df": pos_list})
    
    # Limpeza local
    con.execute("DROP TABLE temp_games; DROP TABLE temp_moves;")
    games_out.unlink()
    moves_out.unlink()
    
    return True

# ==============================================================================
# FASE 2: SINCRONIZAÇÃO DE SHARDS (O CORAÇÃO DO SISTEMA)
# ==============================================================================

def sync_sharded_positions():
    """
    Pega todas as posições acumuladas em 'global_new_positions',
    divide por prefixo, baixa os shards remotos correspondentes,
    funde e sobe de volta.
    """
    
    # 1. Identificar quais prefixos (pastas) foram afetados
    # substring(col, start, length) -> start é 1-based no SQL padrão, mas DuckDB aceita python-slice style às vezes. 
    # Usando sintaxe padrão SQL: 1, 2 pega os dois primeiros chars.
    print("Analisando prefixos de hash para sincronização...")
    prefixes = con.execute("""
        SELECT DISTINCT substring(fen_hash, 1, 2) 
        FROM global_new_positions
    """).fetchall()
    
    prefixes = [row[0] for row in prefixes]
    total_shards = len(prefixes)
    print(f"Total de shards (pastas) a atualizar: {total_shards}")

    for i, prefix in enumerate(prefixes):
        print(f"[{i+1}/{total_shards}] Sincronizando shard: {prefix}...")
        
        remote_path = f"positions/prefix={prefix}/data.parquet"
        local_shard_path = TEMP_DIR / f"shard_{prefix}.parquet"
        
        # A. Preparar dados novos APENAS deste prefixo
        # Usamos GROUP BY para deduplicar as posições novas entre si antes de fundir com o remoto
        con.execute(f"""
            CREATE OR REPLACE TABLE current_new_batch AS 
            SELECT DISTINCT fen_hash, fen_str 
            FROM global_new_positions 
            WHERE substring(fen_hash, 1, 2) = '{prefix}'
        """)

        # B. Baixar dados antigos (se existirem)
        has_remote = False
        try:
            hf_hub_download(
                repo_id=DATASET_REPO,
                filename=remote_path,
                local_dir=TEMP_DIR,
                local_dir_use_symlinks=False
            )
            # Carrega o parquet baixado numa tabela DuckDB
            # O nome do arquivo baixado mantém a estrutura de pastas
            downloaded_file = TEMP_DIR / remote_path
            con.execute(f"CREATE OR REPLACE TABLE remote_shard AS SELECT * FROM read_parquet('{downloaded_file}')")
            has_remote = True
        except EntryNotFoundError:
            # Se não existe, cria tabela vazia com a estrutura correta
            con.execute("CREATE OR REPLACE TABLE remote_shard (fen_hash VARCHAR, fen_str VARCHAR)")
        except Exception as e:
            print(f"Erro ao baixar shard {prefix}: {e}")
            continue

        # C. MERGE (Union Distinct)
        # O 'UNION' padrão do SQL já remove duplicatas. O 'UNION ALL' mantém. Queremos remover.
        # Mas para garantir performance e clareza, fazemos SELECT DISTINCT.
        con.execute(f"""
            COPY (
                SELECT DISTINCT fen_hash, fen_str FROM (
                    SELECT * FROM remote_shard
                    UNION ALL
                    SELECT * FROM current_new_batch
                )
            ) TO '{local_shard_path}' (FORMAT 'parquet', CODEC 'ZSTD')
        """)
        
        # D. Upload
        try:
            api.upload_file(
                path_or_fileobj=str(local_shard_path),
                path_in_repo=remote_path,
                repo_id=DATASET_REPO,
                repo_type="dataset"
            )
        except Exception as e:
            print(f"Erro no upload do shard {prefix}: {e}")
        
        # E. Limpeza
        if has_remote:
            (TEMP_DIR / remote_path).unlink()
        local_shard_path.unlink()

# ==============================================================================
# MAIN
# ==============================================================================

def main():
    if TEMP_DIR.exists():
        shutil.rmtree(TEMP_DIR)
    TEMP_DIR.mkdir(parents=True)

    manifest = load_manifest()
    processed_set = set(manifest["tournaments"])
    newly_processed = []

    print(f"Torneios já no histórico: {len(processed_set)}")

    # --- FASE 1: Loop de Torneios ---
    found_files = list(BASE_DIR.glob("*_games.ndjson"))
    print(f"Encontrados {len(found_files)} arquivos na pasta.")

    for ndjson_file in found_files:
        tid = ndjson_file.stem.replace("_games", "")
        
        if tid in processed_set:
            continue
            
        print(f"-> Processando novo torneio: {tid}")
        
        start_t = time.time()
        success = process_tournament_file(ndjson_file)
        
        if success:
            newly_processed.append(tid)
            print(f"   Concluído em {time.time() - start_t:.2f}s")
        else:
            print("   Arquivo vazio ou inválido, pulando.")

    if not newly_processed:
        print("Nenhum torneio novo para processar.")
        return

    # --- FASE 2: Sincronização Global de Posições ---
    count_new_pos = con.execute("SELECT COUNT(*) FROM global_new_positions").fetchone()[0]
    print(f"\nIniciando sincronização de shards. Total de posições acumuladas (raw): {count_new_pos}")
    
    if count_new_pos > 0:
        sync_sharded_positions()
    else:
        print("Estranhamente, nenhuma posição nova foi encontrada.")

    # --- FASE 3: Atualizar Manifesto ---
    manifest["tournaments"].extend(newly_processed)
    save_manifest(manifest)
    
    print("\nProcesso finalizado com sucesso!")
    print(f"Total de torneios adicionados: {len(newly_processed)}")

    # Limpeza final
    shutil.rmtree(TEMP_DIR)

if __name__ == "__main__":
    main()