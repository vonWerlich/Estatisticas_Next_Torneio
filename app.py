import streamlit as st
import pandas as pd
from utils import *
from filters import *
from visualizations import *
from components import *
from layout import *
from pathlib import Path
from chessboard_component import chessboard_component
import chess
import chess.svg
import base64
import re
import datetime

# IMPORTAÇÕES DAS NOSSAS NOVAS VIEWS
from views.home import renderizar_aba_home
from views.torneios import renderizar_aba_torneios
from views.jogadores import renderizar_aba_jogadores
from views.tabuleiro import renderizar_aba_tabuleiro

# ==============================================================================
# CONFIGURAÇÃO DA PÁGINA
# ==============================================================================
try: 
    caminho_logo = Path(__file__).parent / "logo.PNG"
    st.set_page_config(page_title="Estatísticas NEXT", page_icon=str(caminho_logo), layout="wide", initial_sidebar_state="expanded")
except:
    st.set_page_config(page_title="Estatísticas NEXT", layout="wide")

try:
    caminho_logo = Path(__file__).parent / "logo.PNG"
    logo_base64 = img_to_base64(caminho_logo)
    aplicar_estilos_globais(logo_base64)
except:
    pass

try:
    ajustar_layout_principal(padding_top_rem=0, margin_top_rem=-0.9)
except:
    pass

# ==============================================================================
# 1. CARREGAMENTO DOS DADOS E SIDEBAR (FILTROS)
# ==============================================================================
with st.spinner("♙ Conectando ao Banco de Dados..."):
    df_torneios = carregar_dados_gerais()

if df_torneios.empty:
    st.error("⚠️ Banco de dados vazio ou não encontrado.")
    st.stop()

with st.sidebar.container():
    st.header("Filtros Globais")
    
    tipos_disponiveis = df_torneios["tipo"].dropna().unique().tolist()
    
    if "circuito" in df_torneios.columns:
        circuitos_validos = df_torneios[~df_torneios["circuito"].isin(['Ignorado', '', None])]
        conjuntos_disponiveis = circuitos_validos["circuito"].dropna().unique().tolist()
        
        def regra_de_ordem(nome_circuito):
            c_lower = str(nome_circuito).lower()
            if "suíço" in c_lower or "suico" in c_lower or "swiss" in c_lower: return (0, 0, 0, c_lower)
            match = re.search(r"(\d{4})(?:[-_./](\d))?", nome_circuito)
            if match: return (1, -int(match.group(1)), -int(match.group(2)) if match.group(2) else 0, c_lower)
            return (2, 0, 0, c_lower)
        
        conjuntos_disponiveis.sort(key=regra_de_ordem)
    else:
        conjuntos_disponiveis = []

    data_min, data_max = df_torneios["data"].min().date(), df_torneios["data"].max().date()
    st.multiselect("Tipos", options=tipos_disponiveis, key="tipos_key")
    st.multiselect("Circuitos", options=conjuntos_disponiveis, key="conjuntos_key")

    data_min = df_torneios["data"].min().date()
    data_max = df_torneios["data"].max().date()

    # --- TRAVA DE SEGURANÇA PARA DATAS IGUAIS ---
    if data_min == data_max:
        data_max = data_min + datetime.timedelta(days=1)
    # --------------------------------------------
    if "datas_key" not in st.session_state: 
        st.session_state["datas_key"] = (data_min, data_max)
    datas = st.date_input("Data", min_value=data_min, max_value=data_max, key="datas_key")
    datas_selecionadas = st.session_state["datas_key"]
    st.button("❌ Limpar Filtros", on_click=reset_filtros, args=(df_torneios,), key="bt_limpar")

if not isinstance(datas_selecionadas, tuple) or len(datas_selecionadas) != 2:
    st.warning("Selecione um intervalo de datas completo.")
    st.stop()

df_filtrado = aplicar_filtros(df_torneios, tipos=st.session_state["tipos_key"], conjuntos=[], datas=st.session_state["datas_key"])
if st.session_state["conjuntos_key"] and "circuito" in df_filtrado.columns:
    df_filtrado = df_filtrado[df_filtrado["circuito"].isin(st.session_state["conjuntos_key"])]

# ==============================================================================
# 2. NAVEGAÇÃO ESTRUTURADA (LAYOUT FINAL)
# ==============================================================================
tab_home, tab_torneios, tab_jogadores, tab_tabuleiro = st.tabs([
    "🏠 Início", "🏆 Torneios", "👥 Jogadores", "♟️ Tabuleiro"
])

with tab_home:      renderizar_aba_home()
with tab_torneios:  renderizar_aba_torneios(df_filtrado)
with tab_jogadores: renderizar_aba_jogadores(df_filtrado)
with tab_tabuleiro: renderizar_aba_tabuleiro()