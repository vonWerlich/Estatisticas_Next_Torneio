import sqlite3
import pandas as pd
import streamlit as st
import os
import numpy as np
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
        0 as jogos, -- O banco atual não tem count de jogos na tabela tournaments, mas ok
        circuito
    FROM tournaments
    ORDER BY tournament_start_datetime DESC
    """
    
    df = pd.read_sql_query(query, conn)
    conn.close()

    # Tratamento de datas
    if not df.empty:
        df["data"] = pd.to_datetime(df["data"], utc=True).dt.tz_convert("America/Sao_Paulo")

        # CIRCUITO temporario (para o código poder fingir que se "vira" sem mim)
        # A curto prazo isso não causa problemas, se passar mais de 6 meses pode dar problemas
        df['circuito'] = df['circuito'].replace(['', 'None', 'Ignorado'], np.nan)
        df = df.sort_values(by='data', ascending=True)
        df['circuito'] = df.groupby('tipo')['circuito'].ffill()
        df = df.sort_values(by='data', ascending=False)
        df['circuito'] = df['circuito'].fillna('')
        
    
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
        u.rating_classical,
        u.rating_chess960,
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
        s = pd.to_numeric(df["last_seen_api_timestamp"], errors='coerce')
        
        # 2. A PORTA BLINDADA: Só permite números positivos e menores que 1e13 (Ano 2286).
        # Tudo que for negativo gigante ou absurdo vira Nulo (NaN) e é ignorado.
        s = s.where((s > 0) & (s < 4e14))
        
        # 3. Agora converte com 100% de segurança
        df["last_seen_api_timestamp"] = pd.to_datetime(s, unit='ms', errors='coerce')

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

@st.cache_data(ttl="1h")
def carregar_numero_participantes_total_unico():
    if not os.path.exists(DB_FILE):
        return pd.DataFrame()
    conn = get_db_connection()
    # Pega só o necessário: Quem jogou em qual torneio
    df = pd.read_sql_query("SELECT tournament_id, user_id_lichess FROM tournament_results", conn)
    conn.close()
    return df

@st.cache_data(ttl="30m")
def carregar_pontuacoes_vencedores(torneios_ids):
    if not torneios_ids:
        return pd.DataFrame()
    
    conn = get_db_connection()
    placeholders = ",".join(["?"] * len(torneios_ids))
    # NOVA COLUNA AQUI: Adicionado o performance_rating
    query = f"""
    SELECT 
        user_id_lichess as username,
        tournament_id,
        final_rank,
        performance_rating
    FROM tournament_results
    WHERE tournament_id IN ({placeholders})
    """
    df = pd.read_sql_query(query, conn, params=tuple(torneios_ids))
    conn.close()

    # Retorna o DataFrame inteiro com os ranks brutos, a View decide como pontuar!
    return df

# Pode manter a carregar_pontuacoes_vencedores que deixamos apenas com a query

def calcular_pontos_sistema(rank, sis):
    """Regras de pontuação para as diferentes modalidades"""
    if sis == "NEXT (Padrão 10 a 1)":
        return max(0, 11 - rank) if rank <= 10 else 0
    elif sis == "Fórmula 1 (Atual: 25-18-15...)":
        return {1: 25, 2: 18, 3: 15, 4: 12, 5: 10, 6: 8, 7: 6, 8: 4, 9: 2, 10: 1}.get(rank, 0)
    elif sis == "F1 Clássica (Top 6: 10-6-4...)":
        return {1: 10, 2: 6, 3: 4, 4: 3, 5: 2, 6: 1}.get(rank, 0)
    elif sis == "Pódio Apenas (3-2-1)":
        return {1: 3, 2: 2, 3: 1}.get(rank, 0)
    return 0

@st.cache_data(ttl="15m")
def gerar_ranking_vencedores(df_resultados, sistema, posicoes_extras, mostrar_lanternas, criterio_ordenacao="Pontuação do Torneio", min_torneios=1):
    if df_resultados.empty:
        return pd.DataFrame()
        
    df = df_resultados.copy()
    
    # ---------------------------------------------------------
    # A MÁGICA ACONTECE AQUI: DEFINIÇÃO DO RANKING POR TORNEIO
    # ---------------------------------------------------------
    # Se o critério for performance, recriamos a colocação de cada jogador DENTRO 
    # de cada torneio baseado no seu rating performance real naquela etapa.
    if "Performance" in criterio_ordenacao:
        df['rank_torneio'] = df.groupby('tournament_id')['performance_rating'].rank(ascending=False, method='min')
    else:
        # No modo tradicional, o rank do torneio é a colocação final (final_rank)
        df['rank_torneio'] = df['final_rank']
        
    # Agora calculamos os pontos baseados nesse rank específico!
    df['pontos'] = df['rank_torneio'].apply(lambda x: calcular_pontos_sistema(x, sistema))
    
    # Agrupa os Pontos
    df_ranking_pontos = df.groupby('username')['pontos'].sum().reset_index()
    
    # Agrupa a Performance Média (de todos os torneios jogados, apenas para manter a coluna de exibição)
    df_perf = df.groupby('username')['performance_rating'].mean().fillna(0).reset_index()
    df_perf.rename(columns={'performance_rating': 'Perf. Média'}, inplace=True)
    
    # Conta Assiduidade (Qtd de torneios jogados)
    df_part = df.groupby('username').size().reset_index(name='Qtd. Torneios')
    
    # Conta Medalhas (1º, 2º...) baseadas no RANK ESCOLHIDO (rank_torneio)
    counts = pd.crosstab(df['username'], df['rank_torneio'])
    
    # Mescla tudo em um único DataFrame
    df_ranking = df_ranking_pontos.merge(df_perf, on='username', how='left')
    df_ranking = df_ranking.merge(df_part, on='username', how='left')
    
    # Anexa as colunas de Posição solicitadas
    for i in range(1, posicoes_extras + 1):
        nome_coluna = f"{i}º"
        # O rank pode virar float se houver empate exato de performance, lidamos com isso aqui:
        col_idx = float(i) if float(i) in counts.columns else (i if i in counts.columns else None)
        
        if col_idx is not None:
            df_ranking = df_ranking.merge(counts[[col_idx]].rename(columns={col_idx: nome_coluna}), left_on='username', right_index=True, how='left')
        else:
            df_ranking[nome_coluna] = 0
            
    # Contagem de Lanternas
    if mostrar_lanternas:
        max_ranks = df.groupby('tournament_id')['rank_torneio'].transform('max')
        df['is_lanterna'] = (df['rank_torneio'] == max_ranks) & (df['rank_torneio'] > 1)
        lanternas = df.groupby('username')['is_lanterna'].sum().reset_index()
        df_ranking = df_ranking.merge(lanternas, on='username', how='left')
        df_ranking.rename(columns={'is_lanterna': '🐢 Lanterna'}, inplace=True)
    
    # Excluímos quem zerou e aplicamos o filtro "Tirar Turistas"
    df_ranking = df_ranking[df_ranking['pontos'] > 0]
    df_ranking = df_ranking[df_ranking['Qtd. Torneios'] >= min_torneios]
    
    if df_ranking.empty:
        return pd.DataFrame()
        
    df_ranking = df_ranking.fillna(0)
    
    # Como a nova lógica da coluna "Pontos" já encapsula a Performance se ela foi escolhida,
    # a ordenação base não precisa ter condicionais: sempre Pontos -> Ouros -> Pratas -> etc.
    cols_desempate = [f"{i}º" for i in range(1, posicoes_extras + 1)]
    cols_ordenacao = ['pontos'] + [c for c in cols_desempate if c in df_ranking.columns] + ['Perf. Média', 'Qtd. Torneios']
        
    df_ranking = df_ranking.sort_values(by=cols_ordenacao, ascending=[False] * len(cols_ordenacao))
    
    # Formatações para a tabela exibir números inteiros limpos
    df_ranking['pontos'] = df_ranking['pontos'].astype(int)
    df_ranking['Perf. Média'] = df_ranking['Perf. Média'].astype(int)
    for c in cols_desempate:
        if c in df_ranking.columns:
            df_ranking[c] = df_ranking[c].astype(int)
    if mostrar_lanternas and '🐢 Lanterna' in df_ranking.columns:
        df_ranking['🐢 Lanterna'] = df_ranking['🐢 Lanterna'].astype(int)
    
    return df_ranking

__all__ = [
    "get_db_connection",
    "carregar_dados_gerais",
    "carregar_dados_jogadores_sql",
    "carregar_detalhes_torneio_sql",
    "carregar_games_ndjson",
    "img_to_base64",
    "carregar_numero_participantes_total_unico",
    "carregar_pontuacoes_vencedores",
    "calcular_pontos_sistema",
    "gerar_ranking_vencedores"
]