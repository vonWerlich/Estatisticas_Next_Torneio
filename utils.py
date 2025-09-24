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

__all__ = ["carregar_info", "carregar_results", "carregar_games", "listar_torneios", "img_to_base64"]