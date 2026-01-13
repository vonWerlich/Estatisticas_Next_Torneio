import json
import hashlib
import pathlib
from datetime import datetime
import os

import chess
import pyarrow as pa
import pyarrow.parquet as pq
from huggingface_hub import HfApi, hf_hub_download

# =========================================================
# CONFIG
# =========================================================

DATASET = "vonWerlich/NEXT_Xadrez_Lichess_tournaments"
BASE_DIR = pathlib.Path("torneiosnew")
META_DIR = pathlib.Path("meta")
MANIFEST_FILE = META_DIR / "processed_tournaments.json"

token = os.getenv("HF_TOKEN_LICHESS")
if not token:
    raise RuntimeError("HF_TOKEN_LICHESS não definido no ambiente")

api = HfApi(token=token)

# =========================================================
# FEN utilities
# =========================================================

def canonical_fen(board: chess.Board) -> str:
    fen = board.fen()
    parts = fen.split(" ")
    return " ".join(parts[:4])  # pieces / turn / castling / ep


def fen_hash(fen: str) -> str:
    return hashlib.sha1(fen.encode("utf-8")).hexdigest()

# =========================================================
# Manifest utilities
# =========================================================

def load_manifest():
    """
    Baixa o manifesto do HF se existir.
    Caso contrário, cria um vazio.
    """
    META_DIR.mkdir(exist_ok=True)

    try:
        hf_hub_download(
            repo_id=DATASET,
            repo_type="dataset",
            filename="meta/processed_tournaments.json",
            local_dir="."
        )
        with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"tournaments": []}


def save_manifest(manifest):
    with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    api.upload_file(
        path_or_fileobj=str(MANIFEST_FILE),
        path_in_repo="meta/processed_tournaments.json",
        repo_id=DATASET,
        repo_type="dataset"
    )

# =========================================================
# Tournament year
# =========================================================

def tournament_year(tournament_id: str) -> int:
    info_file = BASE_DIR / f"{tournament_id}_info.json"
    with open(info_file, "r", encoding="utf-8") as f:
        info = json.load(f)

    dt = datetime.fromisoformat(info["startsAt"].replace("Z", "+00:00"))
    return dt.year

# =========================================================
# Process one tournament
# =========================================================

def process_tournament(ndjson_file: pathlib.Path):
    """
    Retorna:
      positions: dict[fen_hash] -> fen_canonical
      hits: list of (fen_hash, game_id, ply, next_san)
    """
    positions = {}
    hits = []

    with open(ndjson_file, "r", encoding="utf-8") as f:
        for line in f:
            game = json.loads(line)

            game_id = game["id"]
            moves = game["moves"].split()

            board = chess.Board()
            ply = 0

            for san in moves:
                fen = canonical_fen(board)
                h = fen_hash(fen)

                positions[h] = fen
                hits.append((h, game_id, ply, san))

                try:
                    board.push_san(san)
                except Exception:
                    break

                ply += 1

    return positions, hits

# =========================================================
# MAIN
# =========================================================

def main():
    manifest = load_manifest()
    already_done = set(manifest["tournaments"])

    print(f"Torneios já processados: {len(already_done)}")

    yearly_positions = {}
    yearly_hits = {}
    newly_processed = []

    for ndjson in BASE_DIR.glob("*_games.ndjson"):
        tournament_id = ndjson.stem.replace("_games", "")

        if tournament_id in already_done:
            continue  # INCREMENTAL: pula completamente

        print(f"Processando torneio novo: {tournament_id}")

        year = tournament_year(tournament_id)
        pos, hits = process_tournament(ndjson)

        yearly_positions.setdefault(year, {}).update(pos)
        yearly_hits.setdefault(year, []).extend(hits)

        newly_processed.append(tournament_id)

    if not newly_processed:
        print("Nenhum torneio novo encontrado.")
        return

    # -----------------------------
    # Write & upload parquet files
    # -----------------------------
    for year, pos_map in yearly_positions.items():
        hits = yearly_hits[year]

        pos_table = pa.table({
            "fen_hash": list(pos_map.keys()),
            "fen_canonical": list(pos_map.values())
        })

        hits_table = pa.table({
            "fen_hash": [h for h, _, _, _ in hits],
            "game_id":  [g for _, g, _, _ in hits],
            "ply":      [p for _, _, p, _ in hits],
            "next_san": [m for _, _, _, m in hits],
        })

        out_dir = pathlib.Path(f"positions/{year}")
        out_dir.mkdir(parents=True, exist_ok=True)

        pos_file = out_dir / "positions.parquet"
        hits_file = out_dir / "position_hits.parquet"

        pq.write_table(pos_table, pos_file)
        pq.write_table(hits_table, hits_file)

        api.upload_file(
            path_or_fileobj=str(pos_file),
            path_in_repo=f"positions/{year}/positions.parquet",
            repo_id=DATASET,
            repo_type="dataset"
        )

        api.upload_file(
            path_or_fileobj=str(hits_file),
            path_in_repo=f"positions/{year}/position_hits.parquet",
            repo_id=DATASET,
            repo_type="dataset"
        )

    # -----------------------------
    # Update manifest
    # -----------------------------
    manifest["tournaments"].extend(newly_processed)
    save_manifest(manifest)

    print(f"Torneios adicionados nesta execução: {len(newly_processed)}")

if __name__ == "__main__":
    main()
