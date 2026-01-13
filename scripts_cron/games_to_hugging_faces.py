import json
import hashlib
import pathlib
from datetime import datetime
import os
import urllib.request

import chess
import chess.pgn
import pyarrow as pa
import pyarrow.parquet as pq
from huggingface_hub import HfApi

# =========================================================
# CONFIG
# =========================================================

DATASET = "vonWerlich/NEXT_Xadrez_Lichess_tournaments"
BASE_DIR = pathlib.Path("torneiosnew")

ECO_PGN_URL  = "https://raw.githubusercontent.com/niklasf/eco/master/eco.pgn"
ECO_PGN_FILE = pathlib.Path("eco.pgn")

token = os.getenv("HF_TOKEN_LICHESS")
if not token:
    raise RuntimeError("HF_TOKEN_LICHESS não definido no ambiente")

api = HfApi(token=token)

# =========================================================
# >>> RESET TOTAL DO DATASET (NOVO) <<<
# =========================================================

print("Apagando dataset no Hugging Face...")
api.delete_repo(
    repo_id=DATASET,
    repo_type="dataset",
)

print("Recriando dataset vazio...")
api.create_repo(
    repo_id=DATASET,
    repo_type="dataset",
    exist_ok=True
)

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
# ECO utilities
# =========================================================

def ensure_eco_pgn():
    if ECO_PGN_FILE.exists():
        return
    print("Baixando eco.pgn...")
    urllib.request.urlretrieve(ECO_PGN_URL, ECO_PGN_FILE)


def load_eco_positions():
    """
    Retorna:
      dict[fen_hash] -> (eco_code, opening_name, depth)
    """
    ensure_eco_pgn()

    eco_map = {}

    with open(ECO_PGN_FILE, encoding="utf-8") as f:
        while True:
            game = chess.pgn.read_game(f)
            if game is None:
                break

            eco     = game.headers.get("ECO")
            opening = game.headers.get("Opening")

            board = game.board()
            depth = 0

            for move in game.mainline_moves():
                board.push(move)
                depth += 1

                fen = canonical_fen(board)
                h   = fen_hash(fen)

                # mantém a menor profundidade conhecida
                if h not in eco_map or depth < eco_map[h][2]:
                    eco_map[h] = (eco, opening, depth)

    return eco_map

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
            moves   = game["moves"].split()

            board = chess.Board()
            ply   = 0

            for san in moves:
                fen = canonical_fen(board)
                h   = fen_hash(fen)

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
    # -----------------------------
    # ECO (base teórica)
    # -----------------------------
    eco_positions = load_eco_positions()

    eco_table = pa.table({
        "fen_hash":     list(eco_positions.keys()),
        "eco":          [v[0] for v in eco_positions.values()],
        "opening_name": [v[1] for v in eco_positions.values()],
        "depth":        [v[2] for v in eco_positions.values()],
    })

    eco_dir = pathlib.Path("eco")
    eco_dir.mkdir(exist_ok=True)

    eco_file = eco_dir / "eco_positions.parquet"
    pq.write_table(eco_table, eco_file)

    api.upload_file(
        path_or_fileobj=str(eco_file),
        path_in_repo="eco/eco_positions.parquet",
        repo_id=DATASET,
        repo_type="dataset"
    )

    # -----------------------------
    # Torneios reais
    # -----------------------------
    yearly_positions = {}
    yearly_hits = {}

    for ndjson in BASE_DIR.glob("*_games.ndjson"):
        tid  = ndjson.stem.replace("_games", "")
        year = tournament_year(tid)

        pos, hits = process_tournament(ndjson)

        yearly_positions.setdefault(year, {}).update(pos)
        yearly_hits.setdefault(year, []).extend(hits)

    for year, pos_map in yearly_positions.items():
        hits = yearly_hits[year]

        pos_table = pa.table({
            "fen_hash":      list(pos_map.keys()),
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

        pos_file  = out_dir / "positions.parquet"
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
