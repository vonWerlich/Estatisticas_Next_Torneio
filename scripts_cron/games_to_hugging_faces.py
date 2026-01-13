import json
import hashlib
import pathlib
from datetime import datetime
import os

import chess
import pyarrow as pa
import pyarrow.parquet as pq
from huggingface_hub import HfApi

# =====================================================
# Configuração
# =====================================================

DATASET = "vonWerlich/NEXT_Xadrez_Lichess_tournaments"
BASE_DIR = pathlib.Path("torneiosnew")

token = os.getenv("HF_TOKEN_LICHESS")
if not token:
    raise RuntimeError("HF_TOKEN_LICHESS não definido no ambiente")

api = HfApi(token=token)

# =====================================================
# Utilidades FEN
# =====================================================

def canonical_fen(board: chess.Board) -> str:
    fen = board.fen()
    return " ".join(fen.split(" ")[:4])


def fen_hash(fen: str) -> str:
    return hashlib.sha1(fen.encode("utf-8")).hexdigest()


# =====================================================
# Ano do torneio
# =====================================================

def tournament_year(tournament_id: str) -> int:
    info_file = BASE_DIR / f"{tournament_id}_info.json"
    with open(info_file, "r", encoding="utf-8") as f:
        info = json.load(f)

    dt = datetime.fromisoformat(info["startsAt"].replace("Z", "+00:00"))
    return dt.year


# =====================================================
# Processamento de um torneio
# =====================================================

def process_tournament(ndjson_file: pathlib.Path):
    """
    Retorna:
      positions: dict[fen_hash] -> fen_canonical
      hits: list[(fen_hash, game_id, ply, next_san)]
      games: list[dict] (ratings e metadados do jogo)
    """
    positions = {}
    hits = []
    games = []

    tid = ndjson_file.stem.replace("_games", "")
    year = tournament_year(tid)

    with open(ndjson_file, "r", encoding="utf-8") as f:
        for line in f:
            game = json.loads(line)

            game_id = game["id"]
            moves = game["moves"].split()

            # -------- ratings / metadados do jogo --------
            white = game["players"]["white"]
            black = game["players"]["black"]

            white_rating = white.get("rating")
            black_rating = black.get("rating")

            avg_rating = (
                (white_rating + black_rating) / 2
                if white_rating is not None and black_rating is not None
                else None
            )

            games.append({
                "game_id": game_id,
                "white_rating": white_rating,
                "black_rating": black_rating,
                "avg_rating": avg_rating,
                "variant": game.get("variant"),
                "perf": game.get("perf"),
                "rated": game.get("rated", False),
                "tournament_id": tid,
                "year": year,
            })

            # -------- posições --------
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

    return positions, hits, games


# =====================================================
# Pipeline principal
# =====================================================

def main():
    yearly_positions = {}
    yearly_hits = {}
    all_games = []

    for ndjson in BASE_DIR.glob("*_games.ndjson"):
        tid = ndjson.stem.replace("_games", "")
        year = tournament_year(tid)

        pos, hits, games = process_tournament(ndjson)

        yearly_positions.setdefault(year, {}).update(pos)
        yearly_hits.setdefault(year, []).extend(hits)
        all_games.extend(games)

    # -----------------------------
    # Escrita + upload POSIÇÕES
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
    # Escrita + upload GAMES
    # -----------------------------
    if all_games:
        games_table = pa.Table.from_pylist(all_games)

        games_dir = pathlib.Path("games")
        games_dir.mkdir(exist_ok=True)

        games_file = games_dir / "games.parquet"
        pq.write_table(games_table, games_file)

        api.upload_file(
            path_or_fileobj=str(games_file),
            path_in_repo="games/games.parquet",
            repo_id=DATASET,
            repo_type="dataset"
        )


if __name__ == "__main__":
    main()
