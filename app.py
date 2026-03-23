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

# ==============================================================================
# CONFIGURAÇÃO DA PÁGINA
# ==============================================================================
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

# AJUSTE DE ALTURA: Voltando para 0 (topo colado)
try:
    ajustar_layout_principal(padding_top_rem=0, margin_top_rem=-0.9)
except:
    pass

# ==============================================================================
# 1. CARREGAMENTO DOS DADOS
# ==============================================================================
with st.spinner("♙ Conectando ao Banco de Dados..."):
    df_torneios = carregar_dados_gerais()

if df_torneios.empty:
    st.error("⚠️ Banco de dados vazio ou não encontrado em `data/team_users.db`.")
    st.info("Execute o script `fix_history.py` primeiro para popular os dados.")
    st.stop()

# ==============================================================================
# 2. SIDEBAR (FILTROS GERAIS)
# ==============================================================================
filters_container = st.sidebar.container()

with filters_container:
    st.header("Filtros Globais")
    
    tipos_disponiveis = df_torneios["tipo"].dropna().unique().tolist()
    
    # 1. Puxa os circuitos reais do banco, ignorando os nulos e os que você marcou como 'Ignorado'
    if "circuito" in df_torneios.columns:
        circuitos_validos = df_torneios[~df_torneios["circuito"].isin(['Ignorado', '', None])]
        conjuntos_disponiveis = circuitos_validos["circuito"].dropna().unique().tolist()
        
        # --- NOVA LÓGICA DE ORDENAÇÃO CUSTOMIZADA ---
        def regra_de_ordem(nome_circuito):
            c_lower = str(nome_circuito).lower()
            
            # Prioridade 0: Suíços (Tudo que tiver "suíço", "suico" ou "swiss" no nome)
            if "suíço" in c_lower or "suico" in c_lower or "swiss" in c_lower:
                return (0, 0, 0, c_lower)
            
            # Prioridade 1: Anos e Semestres (Busca padrão como 2024-2, 2023-1 ou apenas 2020)
            match = re.search(r"(\d{4})(?:[-_./](\d))?", nome_circuito)
            if match:
                ano = int(match.group(1))
                # Se não tiver semestre (ex: apenas 2020), assume 0
                semestre = int(match.group(2)) if match.group(2) else 0 
                
                # Usamos valores negativos (-ano, -semestre) para forçar a ordem decrescente!
                return (1, -ano, -semestre, c_lower)
            
            # Prioridade 2: Todo o resto (Ordem alfabética normal)
            return (2, 0, 0, c_lower)
        
        # Aplica a nossa regra para ordenar a lista
        conjuntos_disponiveis.sort(key=regra_de_ordem)
        # --------------------------------------------
    else:
        conjuntos_disponiveis = []

    data_min, data_max = df_torneios["data"].min().date(), df_torneios["data"].max().date()

    tipos_selecionados = st.multiselect("Tipos", options=tipos_disponiveis, key="tipos_key")
    conjuntos_selecionados = st.multiselect("Circuitos", options=conjuntos_disponiveis, key="conjuntos_key")

    if "datas_key" not in st.session_state:
        st.session_state["datas_key"] = (data_min, data_max)

    datas = st.date_input("Data", min_value=data_min, max_value=data_max, key="datas_key")
    datas_selecionadas = st.session_state["datas_key"]
    
    st.button("❌ Limpar Filtros", on_click=reset_filtros, args=(df_torneios,), key="bt_limpar")

# ==============================================================================
# 3. LÓGICA DE FILTRAGEM
# ==============================================================================
if not isinstance(datas_selecionadas, tuple) or len(datas_selecionadas) != 2:
    st.warning("Selecione um intervalo de datas completo.")
    st.stop()

df_filtrado = aplicar_filtros(
    df_torneios,
    tipos=st.session_state["tipos_key"],
    conjuntos=[], # <--- Não cuida mais disso
    datas=st.session_state["datas_key"]
)

if st.session_state["conjuntos_key"] and "circuito" in df_filtrado.columns:
    df_filtrado = df_filtrado[df_filtrado["circuito"].isin(st.session_state["conjuntos_key"])]

# ==============================================================================
# 4. NAVEGAÇÃO ESTRUTURADA (LAYOUT FINAL)
# ==============================================================================

# Abas Principais
tab_home, tab_torneios_main, tab_jogadores, tab_tabuleiro = st.tabs([
    "🏠 Início", 
    "🏆 Torneios", 
    "👥 Jogadores", 
    "♟️ Tabuleiro"
])

# --- ABA 1: HOME ---
with tab_home:
    # Removemos o bloco de <style> global e o st.title()
    
    # Criamos o título manualmente com HTML para aplicar o estilo SÓ AQUI
    st.markdown(
        '<h1 style="margin-top: -15px; padding-top: 0;">Bem-vindo!</h1>', 
        unsafe_allow_html=True
    )

    st.markdown("""
    Este site tem como objetivo rastrear e fornecer estatísticas sobre os torneios do NEXT - Núcleo de Estudos em Xadrez & Tecnologias.
    
    **O que você encontra aqui:**
    * **🏆 Torneios:** Histórico completo, rankings e partidas.
    * **👥 Jogadores:** Consulta de membros, ratings e atividade.
    * **♟️ Tabuleiro:** Ferramenta de análise integrada.
    * **❓ Em breve:** Mais recursos por vir!
    
    ☝ Utilize as abas no topo para navegar entre diferentes tipos de estatísticas.<br>
    👈 Utilize a barra lateral para aplicar filtros globais.
    <br>
    
    👀 **Links úteis:**<br>
    ♟️ **Equipe no Lichess:** https://lichess.org/team/next-nucleo-de-estudos-em-xadrez--tecnologias<br>
    🏛️ **Página Institucional:** https://www.udesc.br/cct/nextxadrez<br>
    📝 **Blog:** https://nextxadrez.blogspot.com/<br>
    📘 **Facebook:** https://www.facebook.com/nextxadrez<br>
    📷 **Instagram:** https://www.instagram.com/nextxadrez
    """, unsafe_allow_html=True)

# --- ABA 2: TORNEIOS (Com Sub-Abas) ---
with tab_torneios_main:
    # Navegação interna
    sub_aba = st.radio(
        "Navegação Interna:", 
        ["📂 Visão Geral", "📈 Estatísticas", "🔎 Detalhes"], 
        horizontal=True,
        label_visibility="collapsed"
    )
    st.markdown('<hr style="margin-top: -15px; margin-bottom: 15px; border: 0; border-top: 1px solid #808080; opacity: 0.5;">', unsafe_allow_html=True)
    if sub_aba == "📂 Visão Geral":
        st.subheader("Lista de Torneios")
        if not df_filtrado.empty:
            df_show = df_filtrado.copy()
            df_show['id'] = df_show['id'].astype(str)
            st.dataframe(df_show, width=1200, hide_index=True)
        else:
            st.info("Ajuste os filtros na lateral para ver os torneios.")

    elif sub_aba == "📈 Estatísticas":
        st.subheader("Análise Temporal")
        if not df_filtrado.empty:
            # 1. Carrega dados de quem jogou
            df_jogadores = carregar_numero_participantes_total_unico()
            
            # 2. Filtra rapidinho mantendo apenas os torneios atuais da tela
            df_stats = df_jogadores[df_jogadores['tournament_id'].isin(df_filtrado['id'])]

            # 3. Exibe as métricas
            c1, c2, c3 = st.columns(3)
            c1.metric("Torneios Filtrados", len(df_filtrado))
            c2.metric("Total de Participações", len(df_stats)) # Contagem real do banco
            c3.metric("Jogadores Únicos", df_stats['user_id_lichess'].nunique()) # Mágica do Pandas

            # Gráfico (Igual ao original)
            df_grafico = df_filtrado.sort_values(by="data")
            st.bar_chart(df_grafico.set_index("data")["jogadores"])
        else:
            st.info("Sem dados para estatísticas com os filtros atuais.")

    elif sub_aba == "🔎 Detalhes":
        st.subheader("Raio-X do Torneio")
        if not df_filtrado.empty:
            opcoes = df_filtrado.sort_values("data", ascending=False)[["nome", "id"]].values.tolist()
            mapa_nomes = {f"{nome} ({tid})": tid for nome, tid in opcoes}
            
            escolha = st.selectbox("Escolha o Torneio:", options=mapa_nomes.keys())
            
            if escolha:
                tid_selecionado = mapa_nomes[escolha]
                info, df_results = carregar_detalhes_torneio_sql(tid_selecionado)
                
                c1, c2 = st.columns(2)
                with c1:
                    st.write(f"**Sistema:** {info.get('tournament_system')}")
                    st.write(f"**Ritmo:** {info.get('tournament_time_control')}")
                with c2:
                    st.write(f"**Data:** {info.get('tournament_start_datetime')}")
                
                st.divider()

                if not df_results.empty:
                    st.write("#### 🏆 Classificação Final")
                    st.dataframe(df_results, hide_index=True, width='stretch')
                
                df_games = carregar_games_ndjson(tid_selecionado)
                if not df_games.empty:
                    st.write(f"#### ♟️ Jogos ({len(df_games)})")
                    st.dataframe(df_games.head(50), width='stretch')
                else:
                    st.info("Arquivo de jogos detalhados não disponível para este torneio.")
        else:
            st.info("Nenhum torneio disponível para detalhar.")

# --- ABA 3: JOGADORES ---
with tab_jogadores:
    st.subheader("Diretório de Jogadores")
    
    # Carrega todos os jogadores do banco
    df_players_all = carregar_dados_jogadores_sql()
    
    # NOVA LÓGICA: Aplica os filtros globais aos jogadores
    if not df_players_all.empty and not df_filtrado.empty:
        # 1. Pega a relação completa de quem jogou o quê
        df_participacoes = carregar_numero_participantes_total_unico()
        
        # 2. Filtra as participações mantendo apenas os torneios do filtro global
        participacoes_filtradas = df_participacoes[df_participacoes['tournament_id'].isin(df_filtrado['id'])]
        
        # 3. Descobre quem são os jogadores únicos desse recorte temporal/circuito
        jogadores_no_filtro = participacoes_filtradas['user_id_lichess'].unique()
        
        # 4. Filtra a base de jogadores para exibir apenas quem jogou
        df_players = df_players_all[df_players_all['username'].isin(jogadores_no_filtro)].copy()
        
        # 5. BÔNUS: Recalcula a coluna "participacoes" para o escopo filtrado
        contagem_filtrada = participacoes_filtradas.groupby('user_id_lichess').size().reset_index(name='part_filtradas')
        df_players = df_players.merge(contagem_filtrada, left_on='username', right_on='user_id_lichess', how='left')
        df_players['participacoes'] = df_players['part_filtradas'].fillna(0).astype(int)
        df_players = df_players.drop(columns=['part_filtradas'])
        
    else:
        # Se os filtros globais não retornarem torneios, a tabela de jogadores fica vazia
        df_players = pd.DataFrame()

    if not df_players.empty:
        with st.sidebar:
            st.divider()
            st.markdown("### 👤 Filtros de Jogadores")
            
            opcoes_status = df_players["status"].unique().tolist() if "status" in df_players.columns else ["active"]
            
            # Só usa "active" como padrão se existir no banco. Se não, seleciona tudo.
            status_padrao = ["active"] if "active" in opcoes_status else opcoes_status
            
            status_selecionados = st.multiselect(
                "Status da Conta:",
                options=opcoes_status,
                default=status_padrao,
                format_func=lambda x: x.capitalize()
            )
            
            busca_nome = st.text_input("Buscar por nome:", placeholder="Ex: the-chemist")
            
            max_p = int(df_players["participacoes"].max()) if "participacoes" in df_players.columns else 10
            min_part = st.slider("Mínimo de torneios jogados:", 0, max_p, 0)

        df_view = df_players.copy()
        if status_selecionados:
            df_view = df_view[df_view["status"].isin(status_selecionados)]
        if busca_nome:
            df_view = df_view[df_view["username"].str.contains(busca_nome, case=False, na=False)]
        df_view = df_view[df_view["participacoes"] >= min_part]

        c1, c2 = st.columns(2)
        c1.metric("Jogadores Encontrados", len(df_view))
        c2.metric("Total na Base", len(df_players))

        colunas_exibidas = [
            "username",
            "status",
            "last_seen_api_timestamp",
            "rating_blitz",
            "rating_rapid", 
            "rating_chess960",
            "participacoes"
  
        ]

        st.dataframe(
            df_view,
            column_order=colunas_exibidas,
            column_config={
                "username": st.column_config.TextColumn("Jogador", help="ID Lichess"),
                "status": st.column_config.SelectboxColumn("Status", width="small", options=opcoes_status),
                "participacoes": st.column_config.ProgressColumn("Torneios", format="%d", min_value=0, max_value=max_p),
                #ratings
                "rating_blitz": st.column_config.NumberColumn("Blitz", format="%d", help="Rating Blitz"),
                "rating_rapid": st.column_config.NumberColumn("Rapid", format="%d", help="Rating Rápidas"),
                "rating_chess960": st.column_config.NumberColumn("Chess 960", format="%d", help="Rating Xadrez 960 (Fischer Random)"),
                "rating_classical": st.column_config.NumberColumn("Classical", format="%d", help="Rating Clássicas"),
                "rating_bullet": st.column_config.NumberColumn("Bullet", format="%d", help="Rating Bullet"),
                "last_seen_api_timestamp": st.column_config.DatetimeColumn("Visto por último", format="D MMM YYYY", help="Última data que apareceu no Lichess"),
                "user_id_lichess": st.column_config.TextColumn("ID Usuário", help="ID único do usuário no Lichess")
            },
            hide_index=True,
            width='stretch',
            height=600
        )
    else:
        st.info("Nenhum jogador encontrado no banco de dados.")

# --- ABA 4: TABULEIRO ---
with tab_tabuleiro:
    st.subheader("Tabuleiro de Análise")

    if "fen" not in st.session_state:
        st.session_state["fen"] = chess.STARTING_FEN

    try:
        move_data = chessboard_component(
            fen=st.session_state["fen"],
            key="analysis_board"
        )
        if move_data:
            pass

    except ImportError:
        st.warning("Componente 'chessboard_component' não encontrado. Usando visualização estática.")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            board = chess.Board(st.session_state["fen"])
            boardsvg = chess.svg.board(board=board, size=600)
            b64 = base64.b64encode(boardsvg.encode("utf-8")).decode("utf-8")
            st.markdown(f'<img src="data:image/svg+xml;base64,{b64}" width="100%"/>', unsafe_allow_html=True)
        
        with col2:
            st.markdown("#### Controles")
            board = chess.Board(st.session_state["fen"])
            
            if st.button("⬅️ Desfazer Lance", width='stretch'):
                if board.move_stack: 
                    board.pop() 
                    st.session_state["fen"] = board.fen()
                    st.rerun()
            
            if st.button("🔄 Reiniciar Jogo", width='stretch'):
                st.session_state["fen"] = chess.STARTING_FEN
                st.rerun()

            st.text_area("FEN Atual", value=st.session_state['fen'], height=70)