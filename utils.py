import sqlite3
import pandas as pd
import streamlit as st
import os
import json
import ndjson
import base64

# Caminho do banco definido no system_manager.py
DB_FILE = os.path.join("data", "team_users.db")
DATA_DIR_TORNEIOS = os.path.join("data", "raw_tournaments")

def get_db_connection():
    """Abre conexão com o banco no modo de leitura."""
    conn = sqlite3.connect(DB_FILE)
    return conn

@st.cache_data(ttl="1h", show_spinner=False)
def carregar_dados_gerais():
    """
    Carrega o DataFrame principal de torneios para a Visão Geral.
    Faz o trabalho pesado de SQL uma vez e deixa em cache.
    """
    if not os.path.exists(DB_FILE):
        return pd.DataFrame()

    conn = get_db_connection()
    
    # Query que já formata os dados como o app.py espera
    query = """
    SELECT 
        tournament_id as id,
        tournament_name as nome,
        tournament_system as tipo,
        tournament_start_datetime as data,
        number_of_players as jogadores,
        0 as jogos -- O banco atual não tem count de jogos na tabela tournaments, mas ok
    FROM tournaments
    ORDER BY tournament_start_datetime DESC
    """
    
    df = pd.read_sql_query(query, conn)
    conn.close()

    # Tratamento de datas
    if not df.empty:
        df["data"] = pd.to_datetime(df["data"], utc=True).dt.tz_convert("America/Sao_Paulo")
    
    return df

@st.cache_data(ttl="1h")
def carregar_dados_jogadores_sql():
    """
    Carrega a tabela de jogadores direto do SQL.
    Substitui a leitura do players.json.
    """
    if not os.path.exists(DB_FILE):
        return pd.DataFrame()

    conn = get_db_connection()
    
    # Precisamos contar as participações manualmente via SQL, pois é mais rápido
    query = """
    SELECT 
        u.id_lichess as username, -- O App espera 'username'
        u.status,
        u.last_seen_api_timestamp,
        u.rating_blitz,
        u.rating_rapid,
        u.rating_bullet,
        u.bio,
        u.country,
        COUNT(tr.tournament_id) as participacoes
    FROM users u
    LEFT JOIN tournament_results tr ON u.id_lichess = tr.user_id_lichess
    GROUP BY u.id_lichess
    ORDER BY participacoes DESC
    """
    
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    # --- CORREÇÃO DO ERRO DE OVERFLOW ---
    if "last_seen_api_timestamp" in df.columns:
        # 1. Garante que é numérico (transforma lixo em NaN)
        df["last_seen_api_timestamp"] = pd.to_numeric(df["last_seen_api_timestamp"], errors='coerce')
        
        # 2. Filtra números absurdamente grandes que causam o estouro (Overflow)
        # O Pandas suporta datas até o ano ~2262.
        # Em ms, isso é aprox 9.2e12. Vamos cortar qualquer coisa muito acima disso.
        # Valores nulos ou infinitos viram NaT (Not a Time) com segurança.
        
        limite_seguro = 4e14 # Ano ~14.000 (margem de segurança)
        mask_invalido = df["last_seen_api_timestamp"] > limite_seguro
        df.loc[mask_invalido, "last_seen_api_timestamp"] = None
        
        # 3. Agora converte com segurança
        df["last_seen_api_timestamp"] = pd.to_datetime(df["last_seen_api_timestamp"], unit='ms', errors='coerce')

    return df

@st.cache_data(ttl="30m")
def carregar_detalhes_torneio_sql(tid):
    """
    Carrega os resultados de UM torneio específico via SQL.
    """
    conn = get_db_connection()
    
    # Info do Torneio
    q_info = "SELECT * FROM tournaments WHERE tournament_id = ?"
    df_info = pd.read_sql_query(q_info, conn, params=(tid,))
    
    # Resultados (Rankings)
    q_results = """
    SELECT 
        final_rank as rank,
        user_id_lichess as username,
        final_score as score,
        rating_at_start as rating,
        performance_rating as performance
    FROM tournament_results
    WHERE tournament_id = ?
    ORDER BY final_rank ASC
    """
    df_results = pd.read_sql_query(q_results, conn, params=(tid,))
    conn.close()
    
    info_dict = df_info.iloc[0].to_dict() if not df_info.empty else {}
    
    return info_dict, df_results

def carregar_games_ndjson(tid):
    """
    Lê o arquivo de jogos .ndjson do disco (já que não salvamos moves no SQL).
    """
    path = os.path.join(DATA_DIR_TORNEIOS, f"{tid}_games.ndjson")
    if not os.path.exists(path):
        return pd.DataFrame()
    
    try:
        with open(path, "r", encoding="utf-8") as f:
            return pd.DataFrame(ndjson.load(f))
    except:
        return pd.DataFrame()

def img_to_base64(img_path):
    if os.path.exists(img_path):
        with open(img_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""