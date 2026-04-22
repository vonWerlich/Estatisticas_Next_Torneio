# Glorioso script para inserção de dados no Turso!

import os
import sys
import json
import sqlite3
import chess
import time

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

DB_FILE = os.path.join("data", "turso_posicoes.db") 
DATA_DIR_TORNEIOS = os.path.join("data", "raw_tournaments")

def criar_tabelas(conn):
    cur = conn.cursor()
    cur.executescript("""
        CREATE TABLE IF NOT EXISTS posicoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fen_base TEXT UNIQUE
        );
        CREATE TABLE IF NOT EXISTS partidas (
            id TEXT PRIMARY KEY,
            torneio_id TEXT,
            brancas TEXT,
            negras TEXT,
            rating_brancas INTEGER,
            rating_negras INTEGER,
            data TEXT,
            resultado TEXT
        );
        CREATE TABLE IF NOT EXISTS ocorrencias (
            id_posicao INTEGER,
            id_partida TEXT,
            ply INTEGER,
            lance_jogado TEXT, -- <--- NOVA COLUNA (O que jogaram a partir daqui?)
            FOREIGN KEY(id_posicao) REFERENCES posicoes(id),
            FOREIGN KEY(id_partida) REFERENCES partidas(id),
            UNIQUE(id_posicao, id_partida, ply)
        );
        
        CREATE INDEX IF NOT EXISTS idx_fen_base ON posicoes(fen_base);
        CREATE INDEX IF NOT EXISTS idx_posicao_ocorrencia ON ocorrencias(id_posicao);
    """)
    conn.commit()

def extrair_fen_base(fen_completo):
    """Fatia o FEN para remover os contadores de turnos e capturas"""
    partes = fen_completo.split(" ")
    return " ".join(partes[:4])

def processar_jogos():
    print("🚀 Iniciando processamento (Carga Inicial / Atualização Gradual)...")
    
    conn = sqlite3.connect(DB_FILE)
    criar_tabelas(conn)
    cur = conn.cursor()

    # Diff na memória
    print("🔍 Mapeando banco de dados existente para gerar o 'Diff'...")
    cur.execute("SELECT id FROM partidas")
    partidas_ja_processadas = set(row[0] for row in cur.fetchall())
    print(f"   -> {len(partidas_ja_processadas)} partidas já constam na base e serão ignoradas.")

    arquivos = [f for f in os.listdir(DATA_DIR_TORNEIOS) if f.endswith("_games.ndjson")]
    
    novas_partidas_inseridas = 0
    novas_posicoes_inseridas = 0

    for arquivo in arquivos:
        tid = arquivo.split("_")[0]
        caminho = os.path.join(DATA_DIR_TORNEIOS, arquivo)
        
        lote_partidas = []
        lote_fens_unicos = set()
        lote_ocorrencias_temporarias = [] 
        
        with open(caminho, "r", encoding="utf-8") as f:
            for linha in f:
                if not linha.strip(): continue
                
                jogo = json.loads(linha)
                jogo_id = jogo.get("id")
                
                if jogo_id in partidas_ja_processadas:
                    continue
                
                brancas = jogo.get("players", {}).get("white", {}).get("user", {}).get("name", "Unknown").lower()
                negras = jogo.get("players", {}).get("black", {}).get("user", {}).get("name", "Unknown").lower()
                rating_b = jogo.get("players", {}).get("white", {}).get("rating", 0)
                rating_n = jogo.get("players", {}).get("black", {}).get("rating", 0)
                resultado = jogo.get("status") if jogo.get("winner") is None else ("1-0" if jogo.get("winner") == "white" else "0-1")
                if resultado not in ["1-0", "0-1"]: resultado = "1/2-1/2"
                data = jogo.get("createdAt")
                
                lote_partidas.append((jogo_id, tid, brancas, negras, rating_b, rating_n, data, resultado))
                
                # --- MÁGICA DOS LANCES PARA O EXPLORADOR ---
                board = chess.Board()
                moves = jogo.get("moves", "").split(" ")
                
                # Pega a posição inicial antes de qualquer lance
                fen_base = extrair_fen_base(board.fen())
                ply = 0
                
                for move in moves:
                    if not move: continue
                    try:
                        # 1. Lê o lance em formato UCI do Lichess (ex: "e2e4", "e1g1")
                        move_obj = chess.Move.from_uci(move)
                        
                        # 2. Traduz para o formato bonito SAN antes de mexer a peça (ex: "e4", "O-O")
                        lance_bonito_san = board.san(move_obj)
                        
                        # 3. Salva a posição ATUAL e o lance que foi escolhido NELA
                        lote_fens_unicos.add(fen_base)
                        lote_ocorrencias_temporarias.append((fen_base, jogo_id, ply, lance_bonito_san))
                        
                        # 4. Avança o tabuleiro usando o objeto UCI validado
                        board.push(move_obj)
                        fen_base = extrair_fen_base(board.fen())
                        ply += 1
                    except ValueError:
                        break # Ignora lances corrompidos
                
                # E a posição final da partida? (Xeque-mate, empate ou abandono)
                # Ninguém jogou nada a partir dela, então o lance_jogado é None
                lote_fens_unicos.add(fen_base)
                lote_ocorrencias_temporarias.append((fen_base, jogo_id, ply, None))
                
                partidas_ja_processadas.add(jogo_id) 

        if not lote_partidas:
            print(f"   ⏩ Torneio {tid}: Nenhuma partida nova encontrada.")
            continue

        print(f"   💾 Salvando {len(lote_partidas)} partidas inéditas do torneio {tid}...")
        
        cur.executemany("""
            INSERT OR IGNORE INTO partidas (id, torneio_id, brancas, negras, rating_brancas, rating_negras, data, resultado)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, lote_partidas)
        
        fens_tuple = [(f,) for f in lote_fens_unicos]
        cur.executemany("INSERT OR IGNORE INTO posicoes (fen_base) VALUES (?)", fens_tuple)
        
        placeholders = ",".join(["?"] * len(lote_fens_unicos))
        cur.execute(f"SELECT fen_base, id FROM posicoes WHERE fen_base IN ({placeholders})", list(lote_fens_unicos))
        dicionario_ids = {row[0]: row[1] for row in cur.fetchall()}
        
        lote_ocorrencias_final = []
        # ATENÇÃO AQUI: Agora desempacotamos as 4 variáveis!
        for fen_str, p_id, ply, lance_jogado in lote_ocorrencias_temporarias:
            if fen_str in dicionario_ids:
                lote_ocorrencias_final.append((dicionario_ids[fen_str], p_id, ply, lance_jogado))
                
        # INSERT com as 4 colunas!
        cur.executemany("""
            INSERT OR IGNORE INTO ocorrencias (id_posicao, id_partida, ply, lance_jogado)
            VALUES (?, ?, ?, ?)
        """, lote_ocorrencias_final)
        
        conn.commit()
        novas_partidas_inseridas += len(lote_partidas)
        novas_posicoes_inseridas += len(lote_ocorrencias_final)
        
    conn.close()
    print(f"🎉 FINALIZADO! Novas Partidas: {novas_partidas_inseridas} | Novas Posições cruzadas: {novas_posicoes_inseridas}")

if __name__ == "__main__":
    t0 = time.time()
    processar_jogos()
    print(f"⏱️ Tempo total de processamento: {round(time.time() - t0, 2)} segundos")