import streamlit as st
import pandas as pd
from utils import * # Agora usa as novas funções SQL
from filters import *
from visualizations import *
from components import *
from layout import *
from pathlib import Path
from chessboard_component import chessboard_component
import chess
import chess.svg
import base64

# Configuração da Página
try: 
    caminho_logo = Path(__file__).parent / "logo.PNG"
    st.set_page_config(page_title="Estatísticas NEXT", page_icon=str(caminho_logo), layout="wide", initial_sidebar_state="expanded")
except:
    st.set_page_config(page_title="Estatísticas NEXT", layout="wide")

# Estilos e Logo
try:
    caminho_logo = Path(__file__).parent / "logo.PNG"
    logo_base64 = img_to_base64(caminho_logo)
    aplicar_estilos_globais(logo_base64)
except:
    pass

ajustar_layout_principal(padding_top_rem=0, margin_top_rem=0)

# ==============================================================================
# 1. CARREGAMENTO DOS DADOS (AGORA VIA SQL)
# ==============================================================================
with st.spinner("♙ Conectando ao Banco de Dados..."):
    # Carrega a tabela resumo de torneios
    df_torneios = carregar_dados_gerais()

if df_torneios.empty:
    st.error("⚠️ Banco de dados vazio ou não encontrado em `data/team_users.db`.")
    st.info("Execute o script `system_manager.py` primeiro para popular os dados.")
    st.stop()

# ==============================================================================
# 2. SIDEBAR E FILTROS
# ==============================================================================
view_container = st.sidebar.container()
filters_container = st.sidebar.container()

with filters_container:
    st.header("Filtros")
    
    # Filtros baseados no DataFrame carregado do SQL
    tipos_disponiveis = df_torneios["tipo"].dropna().unique().tolist()
    conjuntos_disponiveis = ["Torneios grandes", "Torneios recentes", "Meus favoritos"]
    data_min, data_max = df_torneios["data"].min().date(), df_torneios["data"].max().date()

    tipos_selecionados = st.multiselect("Tipos", options=tipos_disponiveis, key="tipos_key")
    conjuntos_selecionados = st.multiselect("Conjuntos", options=conjuntos_disponiveis, key="conjuntos_key")

    if "datas_key" not in st.session_state:
        st.session_state["datas_key"] = (data_min, data_max)

    datas = st.date_input("Data", min_value=data_min, max_value=data_max, key="datas_key")
    datas_selecionadas = st.session_state["datas_key"]
    
    st.button("❌ Limpar", on_click=reset_filtros, args=(df_torneios,), key="bt_limpar")

with view_container:
    st.header("Menu")
    view_selection = st.radio(
        "Navegação",
        options=['Visão Geral', 'Estatísticas', 'Detalhes do Torneio', 'Jogadores', 'Tabuleiro'],
        label_visibility="collapsed",
        key='view_key'
    )
    st.divider()

# ==============================================================================
# 3. LÓGICA DE EXIBIÇÃO
# ==============================================================================

# Validação de Datas
if not isinstance(datas_selecionadas, tuple) or len(datas_selecionadas) != 2:
    st.warning("Selecione um intervalo de datas completo.")
    st.stop()

# Aplica Filtros (A função aplicar_filtros do filters.py continua funcionando igual, 
# pois mantivemos os nomes das colunas 'data', 'tipo', etc no SQL)
df_filtrado = aplicar_filtros(
    df_torneios,
    tipos=st.session_state["tipos_key"],
    conjuntos=st.session_state["conjuntos_key"],
    datas=st.session_state["datas_key"]
)

if df_filtrado.empty:
    st.warning("Nenhum torneio encontrado com esses filtros.")
    st.stop()

# --- PÁGINA: VISÃO GERAL ---
if st.session_state['view_key'] == 'Visão Geral':
    st.subheader("📂 Lista de Torneios")
    # Colocamos id como string para não formatar com vírgula
    df_show = df_filtrado.copy()
    df_show['id'] = df_show['id'].astype(str)
    st.dataframe(df_show, width=1200, hide_index=True)

# --- PÁGINA: ESTATÍSTICAS ---
elif st.session_state['view_key'] == 'Estatísticas':
    st.subheader("📈 Análise Temporal")
    
    col1, col2 = st.columns(2)
    col1.metric("Torneios Filtrados", len(df_filtrado))
    col2.metric("Total de Participações", int(df_filtrado['jogadores'].sum()))

    # Gráficos
    df_grafico = df_filtrado.sort_values(by="data")
    st.bar_chart(df_grafico.set_index("data")["jogadores"])

# --- PÁGINA: DETALHES ---
elif st.session_state['view_key'] == 'Detalhes do Torneio':
    st.subheader("🔎 Raio-X do Torneio")
    
    # Dropdown de seleção
    # Ordenamos por data decrescente para facilitar
    opcoes = df_filtrado.sort_values("data", ascending=False)[["nome", "id"]].values.tolist()
    # Criamos um dict para busca reversa
    mapa_nomes = {f"{nome} ({tid})": tid for nome, tid in opcoes}
    
    escolha = st.selectbox("Escolha o Torneio:", options=mapa_nomes.keys())
    
    if escolha:
        tid_selecionado = mapa_nomes[escolha]
        
        # BUSCA NO SQL AGORA
        info, df_results = carregar_detalhes_torneio_sql(tid_selecionado)
        
        # Exibe Info
        st.write(f"**Sistema:** {info.get('tournament_system')} | **Ritmo:** {info.get('tournament_time_control')}")
        st.write(f"**Data:** {info.get('tournament_start_datetime')}")
        
        # Exibe Resultados
        if not df_results.empty:
            st.subheader("🏆 Classificação")
            st.dataframe(df_results, width='stretch', hide_index=True)
        
        # Carrega Jogos (Arquivo Físico)
        df_games = carregar_games_ndjson(tid_selecionado)
        if not df_games.empty:
            st.subheader(f"♟️ Jogos ({len(df_games)})")
            st.dataframe(df_games.head(50))
        else:
            st.info("Arquivo de jogos detalhados não disponível para este torneio.")

# --- PÁGINA: JOGADORES ---
elif st.session_state['view_key'] == 'Jogadores':
    st.title("🗂️ Diretório de Jogadores")
    
    # 1. Carrega dados do SQL (rápido e em cache)
    df_players = carregar_dados_jogadores_sql()
    
    if not df_players.empty:
        # --- FILTROS LATERAIS (Restaurando o layout original) ---
        with st.sidebar:
            st.divider()
            st.header("Filtros de Jogadores")
            
            # A. Filtro de Status
            # Pega os status únicos que existem no banco para preencher as opções
            opcoes_status = df_players["status"].unique().tolist() if "status" in df_players.columns else ["active"]
            status_selecionados = st.multiselect(
                "Status da Conta:",
                options=opcoes_status,
                default=["active"], # Padrão: mostra só os ativos
                format_func=lambda x: x.capitalize()
            )
            
            # B. Busca por Nome
            busca_nome = st.text_input("Buscar por nome:", placeholder="Ex: the-chemist")
            
            # C. Slider de Participação (Mínimo de torneios)
            max_p = int(df_players["participacoes"].max()) if "participacoes" in df_players.columns else 10
            min_part = st.slider("Mínimo de torneios jogados:", 0, max_p, 0)

        # --- APLICAÇÃO DOS FILTROS (Lógica Pandas em Memória) ---
        # Começa com todos os dados
        df_view = df_players.copy()
        
        # 1. Filtra Status
        if status_selecionados:
            df_view = df_view[df_view["status"].isin(status_selecionados)]
            
        # 2. Filtra Nome (Case Insensitive)
        if busca_nome:
            df_view = df_view[df_view["username"].str.contains(busca_nome, case=False, na=False)]
            
        # 3. Filtra Quantidade de Torneios
        df_view = df_view[df_view["participacoes"] >= min_part]

        # --- EXIBIÇÃO DA TABELA ---
        
        # Métricas rápidas no topo
        c1, c2 = st.columns(2)
        c1.metric("Jogadores Encontrados", len(df_view))
        c2.metric("Total na Base", len(df_players))

        st.dataframe(
            df_view,
            column_config={
                "username": st.column_config.TextColumn("Jogador", help="ID Lichess"),
                "status": st.column_config.SelectboxColumn("Status", width="small", options=opcoes_status),
                "participacoes": st.column_config.ProgressColumn(
                    "Torneios", 
                    format="%d", 
                    min_value=0, 
                    max_value=max_p
                ),
                "rating_blitz": st.column_config.NumberColumn("Blitz", format="%d"),
                "rating_rapid": st.column_config.NumberColumn("Rapid", format="%d"),
                "last_seen_api_timestamp": st.column_config.DatetimeColumn("Visto por último", format="D MMM YYYY")
            },
            hide_index=True,
            width='stretch',
            height=600
        )
    else:
        st.info("Nenhum jogador encontrado. Rode o script de atualização para popular o banco.")

# --- PÁGINA: TABULEIRO ---
elif st.session_state['view_key'] == 'Tabuleiro':
    st.title("♟️ Tabuleiro de Análise")

    # Inicializa o FEN se não existir
    if "fen" not in st.session_state:
        st.session_state["fen"] = chess.STARTING_FEN

    # Tenta importar o componente interativo (seu arquivo original)
    try:
        from chessboard_component import chessboard_component
        
        # O componente retorna um dicionário com o movimento feito pelo usuário
        move_data = chessboard_component(
            fen=st.session_state["fen"],
            key="analysis_board"
        )
        
        # Se o usuário arrastou uma peça, atualizamos o estado interno
        if move_data:
            # Aqui você precisaria processar o 'move_data' para atualizar o FEN
            # Dependendo de como seu componente retorna (FEN string ou objeto de lance)
            # Exemplo genérico:
            # st.session_state["fen"] = move_data.get("fen", st.session_state["fen"])
            pass

    except ImportError:
        st.warning("Componente 'chessboard_component' não encontrado. Usando visualização estática.")
        # Fallback para a imagem estática (Python Chess SVG)
        col1, col2 = st.columns([2, 1])
        with col1:
            board = chess.Board(st.session_state["fen"])
            boardsvg = chess.svg.board(board=board, size=600)
            b64 = base64.b64encode(boardsvg.encode("utf-8")).decode("utf-8")
            st.markdown(f'<img src="data:image/svg+xml;base64,{b64}" width="100%"/>', unsafe_allow_html=True)
        
        with col2:
            st.subheader("Controles")
            board = chess.Board(st.session_state["fen"])
            
            if st.button("⬅️ Desfazer Lance"):
                if board.move_stack: # Lógica simples se tiver stack, senão precisa reconstruir
                    board.pop() 
                    st.session_state["fen"] = board.fen()
                    st.rerun()
            
            if st.button("🔄 Reiniciar"):
                st.session_state["fen"] = chess.STARTING_FEN
                st.rerun()

            st.caption(f"FEN Atual: {st.session_state['fen']}")