# Glorioso script para inserção de dados no Turso CLOUD! (Versão V3 - Cache & Resiliência)

import os
import sys
import json
import chess
import time
from libsql_client import create_client_sync

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

TURSO_URL = os.environ.get("TURSO_URL")
TURSO_TOKEN = os.environ.get("TURSO_TOKEN")

if not TURSO_URL or not TURSO_TOKEN:
    raise ValueError("⚠️ Credenciais do Turso não encontradas nas variáveis de ambiente!")

DATA_DIR_TORNEIOS = os.path.join("data", "raw_tournaments")

def criar_tabelas(client):
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
        "CREATE INDEX IF NOT EXISTS idx_posicao_ocorrencia ON ocorrencias(id_posicao);",
        "CREATE INDEX IF NOT EXISTS idx_partida_ocorrencia ON ocorrencias(id_partida);"
    ])

def extrair_fen_base(fen_completo):
    return " ".join(fen_completo.split(" ")[:4])

def enviar_em_lotes_bulk(client, base_query, dados, tamanho_lote=500, max_tentativas=3):
    """O Bulk Insert: Rápido e à prova de limite de CPU."""
    if not dados: return
    num_cols = len(dados[0])
    linha_ph = "(" + ",".join(["?"] * num_cols) + ")"
    
    for i in range(0, len(dados), tamanho_lote):
        lote = dados[i:i + tamanho_lote]
        args = []
        for tupla in lote: args.extend(tupla)
        
        query = f"{base_query} VALUES {','.join([linha_ph] * len(lote))}"
        
        for tentativa in range(1, max_tentativas + 1):
            try:
                client.execute(query, args)
                time.sleep(0.05)
                break
            except Exception as e:
                if tentativa < max_tentativas:
                    time.sleep(3 * tentativa)
                else:
                    raise e

def contar_banco(client):
    """Conta exatamente quantas linhas existem no banco real."""
    p = client.execute("SELECT COUNT(*) FROM partidas").rows[0][0]
    o = client.execute("SELECT COUNT(*) FROM ocorrencias").rows[0][0]
    return p, o

def processar_jogos():
    print("🚀 Conectando ao Turso Cloud (V3)...")
    client = create_client_sync(url=TURSO_URL, auth_token=TURSO_TOKEN)
    criar_tabelas(client)

    partidas_inicio, ocorrencias_inicio = contar_banco(client)

    # Diff blindado: Só conta como processada se a partida tem ocorrências vinculadas
    print("🔍 Mapeando banco de dados existente...")
    res = client.execute("SELECT DISTINCT id_partida FROM ocorrencias")
    partidas_ja_processadas = set(row[0] for row in res.rows)
    print(f"   -> {len(partidas_ja_processadas)} partidas estão 100% completas na base.")

    # O Super Cache de FENs (Evita round-trips no banco)
    fen_cache = {}

    # A Fila Organizada
    arquivos = sorted([f for f in os.listdir(DATA_DIR_TORNEIOS) if f.endswith("_games.ndjson")])

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
                
                # A barreira: Se já existe, pula TUDO dessa partida
                if jogo_id in partidas_ja_processadas: continue
                
                # Prepara Partida
                brancas = jogo.get("players", {}).get("white", {}).get("user", {}).get("name", "Unknown").lower()
                negras = jogo.get("players", {}).get("black", {}).get("user", {}).get("name", "Unknown").lower()
                rating_b = jogo.get("players", {}).get("white", {}).get("rating", 0)
                rating_n = jogo.get("players", {}).get("black", {}).get("rating", 0)
                resultado = jogo.get("status") if jogo.get("winner") is None else ("1-0" if jogo.get("winner") == "white" else "0-1")
                if resultado not in ["1-0", "0-1"]: resultado = "1/2-1/2"
                
                lote_partidas.append((jogo_id, tid, brancas, negras, rating_b, rating_n, jogo.get("createdAt"), resultado))
                
                # Prepara Lances
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
                
                # Adiciona localmente para não processar a mesma partida duas vezes NO MESMO ARQUIVO
                partidas_ja_processadas.add(jogo_id)

        if not lote_partidas:
            print(f"   ⏩ Torneio {tid}: 100% Concluído.")
            continue

        print(f"   💾 Sincronizando o torneio {tid}...")
        enviar_em_lotes_bulk(client, "INSERT OR IGNORE INTO partidas (id, torneio_id, brancas, negras, rating_brancas, rating_negras, data, resultado)", lote_partidas)
        
        # O PULO DO GATO: Filtra os FENs usando o Super Cache
        fens_inéditos = [f for f in lote_fens_unicos if f not in fen_cache]
        
        if fens_inéditos:
            # 1. Envia só os que a gente nunca viu na vida
            enviar_em_lotes_bulk(client, "INSERT OR IGNORE INTO posicoes (fen_base)", [(f,) for f in fens_inéditos])
            
            # 2. Busca o ID no banco APENAS desses novos e salva no Cache
            for i in range(0, len(fens_inéditos), 500):
                chunk = fens_inéditos[i:i+500]
                placeholders = ",".join(["?"] * len(chunk))
                res = client.execute(f"SELECT fen_base, id FROM posicoes WHERE fen_base IN ({placeholders})", chunk)
                for row in res.rows:
                    fen_cache[row[0]] = row[1]
        
        # Cruza usando o Cache de RAM (Instantâneo!)
        lote_ocorrencias_final = []
        for fen_str, p_id, ply, lance_jogado in lote_ocorrencias_temporarias:
            # Se por acaso algum FEN escapar do cache (erro raro de conexão), ignoramos a ocorrência
            if fen_str in fen_cache:
                lote_ocorrencias_final.append((fen_cache[fen_str], p_id, ply, lance_jogado))
                
        enviar_em_lotes_bulk(client, "INSERT OR IGNORE INTO ocorrencias (id_posicao, id_partida, ply, lance_jogado)", lote_ocorrencias_final)
        
        print(f"      🏆 Torneio atualizado!\n")

    # A MATEMÁTICA REAL E VERDADEIRA
    partidas_fim, ocorrencias_fim = contar_banco(client)
    client.close()
    
    print("\n🎉 RELATÓRIO FINAL:")
    print(f"   Partidas Reais Adicionadas: {partidas_fim - partidas_inicio}")
    print(f"   Lances (Ocorrências) Reais Adicionados: {ocorrencias_fim - ocorrencias_inicio}")

if __name__ == "__main__":
    t0 = time.time()
    processar_jogos()
    print(f"⏱️ Tempo total de processamento: {round(time.time() - t0, 2)} segundos")