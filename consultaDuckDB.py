import duckdb
import hashlib

fen = "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq -"

fen_hash = hashlib.sha1(fen.encode("utf-8")).hexdigest()

con = duckdb.connect()

df = con.execute("""
    SELECT game_id, ply
    FROM read_parquet(
      'https://huggingface.co/datasets/vonWerlich/NEXT_Xadrez_Lichess_tournaments/resolve/main/positions/2021/position_hits.parquet'
    )
    WHERE fen_hash = ?
""", [fen_hash]).df()
