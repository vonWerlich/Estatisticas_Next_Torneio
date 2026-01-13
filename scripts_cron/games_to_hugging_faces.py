import json
import hashlib
import pathlib
from datetime import datetime
import os
import chess
import pyarrow as pa
import pyarrow.parquet as pq
from huggingface_hub import HfApi

DATASET = "vonWerlich/NEXT_Xadrez_Lichess_tournaments"
BASE_DIR = pathlib.Path("torneiosnew")

token = os.getenv("HF_TOKEN_LICHESS")
if not token:
    raise RuntimeError("HF_TOKEN não definido no ambiente")

api = HfApi(token=token)

# -----------------------------
# FEN utilities
# -----------------------------

def canonical_fen(board: chess.Board) -> str:
    fen = board.fen()
    parts = fen.split(" ")
    return " ".join(parts[:4])  # pieces, turn, castling, ep


def fen_hash(fen: str) -> str:
    return hashlib.sha1(fen.encode("utf-8")).hexdigest()


# -----------------------------
# Load year from info.json
# -----------------------------

def tournament_year(tournament_id: str) -> int:
    info_file = BASE_DIR / f"{tournament_id}_info.json"
    with open(info_file, "r", encoding="utf-8") as f:
        info = json.load(f)
    dt = datetime.fromisoformat(info["startsAt"].replace("Z", "+00:00"))
    return dt.year


# -----------------------------
# Process one NDJSON
# -----------------------------

def process_tournament(ndjson_file: pathlib.Path):
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
                try:
                    board.push_san(san)
                except Exception:
                    break

                ply += 1
                fen = canonical_fen(board)
                h = fen_hash(fen)

                positions[h] = fen
                hits.append((h, game_id, ply))

    return positions, hits


# -----------------------------
# Main pipeline
# -----------------------------

def main():
    yearly_positions = {}
    yearly_hits = {}

    for ndjson in BASE_DIR.glob("*_games.ndjson"):
        tid = ndjson.stem.replace("_games", "")
        year = tournament_year(tid)

        pos, hits = process_tournament(ndjson)

        yearly_positions.setdefault(year, {}).update(pos)
        yearly_hits.setdefault(year, []).extend(hits)

    for year, pos_map in yearly_positions.items():
        hits = yearly_hits[year]

        pos_table = pa.table({
            "fen_hash": list(pos_map.keys()),
            "fen_canonical": list(pos_map.values())
        })

        hits_table = pa.table({
            "fen_hash": [h for h, _, _ in hits],
            "game_id": [g for _, g, _ in hits],
            "ply": [p for _, _, p in hits]
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


if __name__ == "__main__":
    main()
