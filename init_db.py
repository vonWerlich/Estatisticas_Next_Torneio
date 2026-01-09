import sqlite3
import sys
import os

# Ajuste de encoding para Windows
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

DB_FILE = "team_users.db"

def run():
    print(f"🛠️ Inicializando banco de dados COMPLETO em: {DB_FILE}")
    
    # Conecta (cria o arquivo se não existir)
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    # Habilita Foreign Keys (boa prática)
    cur.execute("PRAGMA foreign_keys = ON;")

    # ---------------------------------------------------------
    # DEFINIÇÃO DA TABELA (Schema "All-In")
    # ---------------------------------------------------------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        -- === IDENTIFICAÇÃO ===
        id_lichess TEXT PRIMARY KEY,
        username TEXT,
        status TEXT CHECK (status IN ('active', 'inactive', 'banned', 'closed')),
        is_team_member INTEGER DEFAULT 0 CHECK (is_team_member IN (0,1)),

        -- === PERFIL PÚBLICO ===
        bio TEXT,
        country TEXT,
        location TEXT,
        
        -- === RATINGS (PADRÃO) ===
        rating_bullet INTEGER,
        rating_blitz INTEGER,
        rating_rapid INTEGER,
        rating_classical INTEGER,
        rating_correspondence INTEGER,

        -- === RATINGS (VARIANTES) ===
        rating_crazyhouse INTEGER,
        rating_chess960 INTEGER,
        rating_king_of_the_hill INTEGER,
        rating_three_check INTEGER,
        rating_antichess INTEGER,
        rating_atomic INTEGER,
        rating_horde INTEGER,
        rating_racing_kings INTEGER,
        rating_ultra_bullet INTEGER,

        -- === RATINGS (PUZZLES & TREINO) ===
        rating_puzzle INTEGER,         -- Rating Glicko2 de Tática
        
        -- === ESTATÍSTICAS GERAIS ===
        total_games INTEGER,
        total_wins INTEGER,
        total_losses INTEGER,
        total_draws INTEGER,
        play_time_total INTEGER,       -- Tempo total jogado (segundos)

        -- === DATAS E CONTROLE ===
        created_at INTEGER,            -- Timestamp criação da conta
        seen_at INTEGER,               -- Timestamp último login
        last_seen_api_timestamp INTEGER, -- Quando nosso bot atualizou isso
        
        first_seen_team_date TEXT,     -- ISO Date (Entrada na equipe)
        last_seen_team_date TEXT,      -- ISO Date (Última atividade na equipe)

        -- === BACKUP COMPLETO ===
        raw_json TEXT                  -- O JSON puro da API para garantir
    )
    """)

    conn.commit()
    conn.close()
    
    print("✅ Tabela 'users' criada com sucesso!")
    print("   Colunas de rating para TODAS as variantes foram adicionadas.")
    print("   Campos vazios ficarão como NULL automaticamente.")

if __name__ == "__main__":
    run()