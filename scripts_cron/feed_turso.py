# Glorioso script para inserção de dados no Turso CLOUD!

import os
import sys
import json
import chess
import time
from libsql_client import create_client_sync, Statement

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

# Puxa do ambiente (GitHub Secrets ou arquivo .env local)
TURSO_URL = os.environ.get("TURSO_URL")
TURSO_TOKEN = os.environ.get("TURSO_TOKEN")

if not TURSO_URL or not TURSO_TOKEN:
    raise ValueError("⚠️ Credenciais do Turso não encontradas nas variáveis de ambiente!")

DATA_DIR_TORNEIOS = os.path.join("data", "raw_tournaments")

def criar_tabelas(client):
    """Cria a estrutura inicial no Turso caso o banco esteja vazio."""
    # O Turso processa transações atômicas via batch
    client.batch([
        "CREATE TABLE IF NOT EXISTS posicoes (id INTEGER PRIMARY KEY AUTOINCREMENT, fen_base TEXT UNIQUE);",
        """CREATE TABLE IF NOT EXISTS partidas (
            id TEXT PRIMARY KEY, torneio_id TEXT, brancas TEXT, negras TEXT,
            rating_brancas INTEGER, rating_negras INTEGER, data TEXT, resultado TEXT
        );""",
        """CREATE TABLE IF NOT EXISTS ocorrencias (
            id_posicao INTEGER, id_partida TEXT, ply INTEGER, lance_jogado TEXT,
            FOREIGN KEY(id_posicao) REFERENCES posicoes(id),
            FOREIGN KEY(id_partida) REFERENCES partidas(id),
            UNIQUE(id_posicao, id_partida, ply)
        );""",
        "CREATE INDEX IF NOT EXISTS idx_fen_base ON posicoes(fen_base);",
        "CREATE INDEX IF NOT EXISTS idx_posicao_ocorrencia ON ocorrencias(id_posicao);"
    ])

def extrair_fen_base(fen_completo):
    partes = fen_completo.split(" ")
    return " ".join(partes[:4])

def enviar_em_lotes(client, query, dados, tamanho_lote=1000):
    """Envia dados para o Turso em pequenos pacotes para não estourar o limite da API."""
    for i in range(0, len(dados), tamanho_lote):
        lote = dados[i:i + tamanho_lote]
        statements = [Statement(query, list(linha)) for linha in lote]
        client.batch(statements)

def processar_jogos():
    print("🚀 Conectando ao Turso Cloud...")
    client = create_client_sync(url=TURSO_URL, auth_token=TURSO_TOKEN)
    
    criar_tabelas(client)

    # Diff na nuvem
    print("🔍 Mapeando banco de dados existente para gerar o 'Diff'...")
    res = client.execute("SELECT id FROM partidas")
    partidas_ja_processadas = set(row[0] for row in res.rows)
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
                
                board = chess.Board()
                moves = jogo.get("moves", "").split(" ")
                
                fen_base = extrair_fen_base(board.fen())
                ply = 0
                
                for move in moves:
                    if not move: continue
                    try:
                        lance_parseado = board.parse_san(move)
                        lance_bonito_san = board.san(lance_parseado)
                        
                        lote_fens_unicos.add(fen_base)
                        lote_ocorrencias_temporarias.append((fen_base, jogo_id, ply, lance_bonito_san))
                        
                        board.push(lance_parseado)
                        fen_base = extrair_fen_base(board.fen())
                        ply += 1
                    except ValueError:
                        break
                
                lote_fens_unicos.add(fen_base)
                lote_ocorrencias_temporarias.append((fen_base, jogo_id, ply, None))
                partidas_ja_processadas.add(jogo_id) 

        if not lote_partidas:
            print(f"   ⏩ Torneio {tid}: Nenhuma partida nova encontrada.")
            continue

        print(f"   💾 Sincronizando o torneio {tid} com a nuvem...")
        
        # 1. Envia as Partidas
        enviar_em_lotes(client, 
            "INSERT OR IGNORE INTO partidas (id, torneio_id, brancas, negras, rating_brancas, rating_negras, data, resultado) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
            lote_partidas
        )
        
        # 2. Envia os FENs Únicos
        fens_lista = [(f,) for f in lote_fens_unicos]
        enviar_em_lotes(client, "INSERT OR IGNORE INTO posicoes (fen_base) VALUES (?)", fens_lista)
        
        # 3. Recupera os IDs gerados no banco para os FENs (Em lotes para não quebrar o limite de variáveis do IN clause)
        dicionario_ids = {}
        fens_array = list(lote_fens_unicos)
        for i in range(0, len(fens_array), 500):
            chunk = fens_array[i:i+500]
            placeholders = ",".join(["?"] * len(chunk))
            res = client.execute(f"SELECT fen_base, id FROM posicoes WHERE fen_base IN ({placeholders})", chunk)
            for row in res.rows:
                dicionario_ids[row[0]] = row[1]
        
        # 4. Prepara as ocorrências cruzando o texto do FEN com o ID do banco
        lote_ocorrencias_final = []
        for fen_str, p_id, ply, lance_jogado in lote_ocorrencias_temporarias:
            if fen_str in dicionario_ids:
                lote_ocorrencias_final.append((dicionario_ids[fen_str], p_id, ply, lance_jogado))
                
        # 5. Envia as Ocorrências
        enviar_em_lotes(client, 
            "INSERT OR IGNORE INTO ocorrencias (id_posicao, id_partida, ply, lance_jogado) VALUES (?, ?, ?, ?)", 
            lote_ocorrencias_final
        )
        
        novas_partidas_inseridas += len(lote_partidas)
        novas_posicoes_inseridas += len(lote_ocorrencias_final)
        
    client.close()
    print(f"🎉 FINALIZADO! Novas Partidas: {novas_partidas_inseridas} | Novas Posições cruzadas: {novas_posicoes_inseridas}")

if __name__ == "__main__":
    t0 = time.time()
    processar_jogos()
    print(f"⏱️ Tempo total de processamento: {round(time.time() - t0, 2)} segundos")