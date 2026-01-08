import json
import ndjson
import os
import pandas as pd
import base64
import streamlit as st

@st.cache_data(ttl="180d")
def carregar_info(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

@st.cache_data(ttl="180d")
def carregar_results(path):
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

@st.cache_data(ttl="180d")
def carregar_games(path):
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        try:
            return pd.DataFrame(ndjson.load(f))
        except Exception:
            return pd.DataFrame()

def listar_torneios(data_dir):
    torneios = {}
    for fname in os.listdir(data_dir):
        if fname.endswith("_info.json"):
            tid = fname.split("_")[0]
            torneios[tid] = {
                "id": tid,
                "info": os.path.join(data_dir, f"{tid}_info.json"),
                "results": os.path.join(data_dir, f"{tid}_results.json"),
                "games": os.path.join(data_dir, f"{tid}_games.ndjson"),
            }
    return torneios

def img_to_base64(img_path):
    """Converte uma imagem local para uma string base64 para uso em HTML."""
    if os.path.exists(img_path):
        with open(img_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

# stats dos players

@st.cache_data(ttl="1h")
def carregar_dados_jogadores(data_dir_players):
    """
    Carrega players.json e tournament_participants.json.
    Retorna um DataFrame consolidado com contagem de participações.
    """
    path_players = os.path.join(data_dir_players, "players.json")
    path_parts = os.path.join(data_dir_players, "tournament_participants.json")
    
    if not os.path.exists(path_players):
        return pd.DataFrame()

    # 1. Carrega Jogadores
    with open(path_players, "r", encoding="utf-8") as f:
        players = json.load(f)
    
    df = pd.DataFrame(players)
    
    # 2. Carrega Participações e Conta
    if os.path.exists(path_parts):
        with open(path_parts, "r", encoding="utf-8") as f:
            parts_map = json.load(f)
        
        # Conta quantas vezes cada ID aparece nas listas de torneios
        from collections import Counter
        all_ids = []
        for tid, p_ids in parts_map.items():
            all_ids.extend(p_ids)
            
        counts = Counter(all_ids)
        
        # Mapeia a contagem para o DataFrame (usando a coluna 'id')
        df["participacoes"] = df["id"].map(counts).fillna(0).astype(int)
    else:
        df["participacoes"] = 0

    # 3. Adiciona colunas de Placeholder para Ratings (Futuro)
    # Isso garante que a tabela já tenha a "cara" final
    cols_futuras = ["rating_blitz", "rating_bullet", "rating_rapid"]
    for col in cols_futuras:
        if col not in df.columns:
            df[col] = None # Vazio por enquanto

    return df

__all__ = ["carregar_info", "carregar_results", "carregar_games", "listar_torneios", "img_to_base64",
           "carregar_dados_jogadores", ]