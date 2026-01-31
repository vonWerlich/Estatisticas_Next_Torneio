-- Tabela Mestre de Usuários
-- Armazena tanto membros atuais, ex-membros e lurkers
CREATE TABLE IF NOT EXISTS users (
    id_lichess TEXT PRIMARY KEY,

    -- Status e Membresia
    -- 'active' é o padrão para facilitar novos inserts
    status TEXT DEFAULT 'active' CHECK (status IN ('active','inactive','banned','closed')),
    -- 0 = Ex-membro ou nunca foi membro; 1 = Membro atual da equipe
    is_team_member INTEGER DEFAULT 0 CHECK (is_team_member IN (0,1)),

    -- Rastreamento Temporal (Histórico de Torneios)
    first_seen_team_date TEXT,
    last_seen_team_date TEXT,

    -- Controle de Atualização (API)
    last_seen_api_timestamp INTEGER, -- O 'seenAt' vindo do Lichess (quando o cara logou pela ultima vez)
    last_updated_at INTEGER,         -- NOVO: Quando NOSSO script atualizou esse perfil pela última vez (usado na fila de prioridade)

    -- Dados de Perfil
    real_name TEXT,
    country TEXT,
    location TEXT,
    bio TEXT,
    fide_rating INTEGER,

    -- Ratings (Todas as variantes oficiais)
    rating_bullet INTEGER,
    rating_blitz INTEGER,
    rating_rapid INTEGER,
    rating_classical INTEGER,
    rating_ultrabullet INTEGER,
    rating_chess960 INTEGER,
    rating_crazyhouse INTEGER,
    rating_antichess INTEGER,
    rating_atomic INTEGER,
    rating_horde INTEGER,
    rating_racing_kings INTEGER,
    rating_three_check INTEGER,

    -- Metadados do Sistema
    created_at INTEGER
);

-- Tabela de Torneios
-- Armazena os metadados de cada evento (Arena ou Swiss)
CREATE TABLE IF NOT EXISTS tournaments (
    tournament_id TEXT PRIMARY KEY,

    tournament_start_datetime TEXT,   -- startsAt (ISO 8601)
    tournament_system TEXT,           -- arena / swiss
    tournament_time_control TEXT,     -- blitz, rapid, classical
    tournament_variant TEXT,          -- standard, chess960, etc
    tournament_rated INTEGER,         -- 0 ou 1

    number_of_players INTEGER,
    tournament_name TEXT
);

-- Tabela de Resultados
-- Liga Usuários a Torneios (Many-to-Many)
CREATE TABLE IF NOT EXISTS tournament_results (
    tournament_id TEXT,
    user_id_lichess TEXT,

    final_rank INTEGER,
    final_score INTEGER,
    rating_at_start INTEGER,     -- Rating do jogador NO DIA do torneio
    performance_rating INTEGER,

    PRIMARY KEY (tournament_id, user_id_lichess),
    FOREIGN KEY (tournament_id) REFERENCES tournaments(tournament_id),
    FOREIGN KEY (user_id_lichess) REFERENCES users(id_lichess)
);