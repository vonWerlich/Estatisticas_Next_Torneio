users (
    id_lichess TEXT PRIMARY KEY,

    status TEXT CHECK (status IN ('active','inactive','banned','closed')),
    is_team_member INTEGER CHECK (is_team_member IN (0,1)),

    first_seen_team_date TEXT,
    last_seen_team_date TEXT,
    last_seen_api_timestamp INTEGER,

    real_name TEXT,
    country TEXT,
    location TEXT,
    bio TEXT,
    fide_rating INTEGER,

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

    created_at INTEGER
)
tournaments (
    tournament_id TEXT PRIMARY KEY,

    tournament_start_datetime TEXT,   -- startsAt
    tournament_system TEXT,           -- arena / swiss
    tournament_time_control TEXT,     -- blitz, rapid, classical
    tournament_variant TEXT,          -- standard, chess960, etc
    tournament_rated INTEGER,          -- 0/1

    number_of_players INTEGER,
    tournament_name TEXT
)
tournament_results (
    tournament_id TEXT,
    user_id_lichess TEXT,

    final_rank INTEGER,
    final_score INTEGER,
    rating_at_start INTEGER,
    performance_rating INTEGER,

    PRIMARY KEY (tournament_id, user_id_lichess),
    FOREIGN KEY (tournament_id) REFERENCES tournaments(tournament_id),
    FOREIGN KEY (user_id_lichess) REFERENCES users(id_lichess)
)
