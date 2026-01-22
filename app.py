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

DATA_DIR = "torneiosnew"  # pasta onde estão todos os torneios
PLAYERS_DIR = "player_data" # pasta dos jogadores

try: 
    caminho_logo = Path(__file__).parent / "logo.PNG"
    st.set_page_config(
        page_title="Estatísticas NEXT",
        page_icon=caminho_logo,
        layout="wide",
        initial_sidebar_state="expanded"
    )
except FileNotFoundError:
    st.set_page_config(
        page_title="Estatísticas NEXT",
        page_icon="logo.png",
        layout="wide",
        initial_sidebar_state="expanded"
    )

try:
    caminho_logo = Path(__file__).parent / "logo.PNG"
    logo_base64 = img_to_base64(caminho_logo)
    aplicar_estilos_globais(logo_base64)  #  ESTILOS 

except FileNotFoundError:
    st.title("Análise de Dados dos Torneios do NEXT")
    st.error("Arquivo 'logo.png' não encontrado. Alguns estilos não foram aplicados.")

ajustar_layout_principal(padding_top_rem=0, margin_top_rem=0)  # Controla o espaço no topo em rem 

# ---------- Carregar dados ----------

@st.cache_data(ttl="4d", show_spinner=False) # <-- cache para atualização mais rápida, dura 4 dias
def carregar_todos_os_torneios(data_dir):
    """Lê todos os arquivos da pasta e retorna um DataFrame, usando cache."""
    torneios = listar_torneios(data_dir)
    info_list = []
    for tid, paths in torneios.items():
        try:
            info = carregar_info(paths["info"])
            nome = info.get("name") or info.get("fullName") or "Sem nome"
            tipo = info.get("system", "swiss" if "round" in info else "desconhecido")
            data = pd.to_datetime(info.get("startsAt"), errors="coerce", utc=True)
            data = data.tz_convert("America/Sao_Paulo")
            info_list.append({
                "id": tid, "nome": nome, "tipo": tipo, "criador": info.get("createdBy"),
                "data": data, "jogadores": info.get("nbPlayers", None),
                "jogos": info.get("stats", {}).get("games", None)
            })
        except Exception:
            # Silenciosamente ignora arquivos com erro no carregamento em cache
            continue
    df = pd.DataFrame(info_list)
    return df, torneios 

with st.spinner("♙♘♗♖♕♔ Aguarde, preparando as estatísticas de todos os torneios... ♟♞♝♜♛♚"):
    #nova mensagem de erro
    df_torneios, torneios = carregar_todos_os_torneios(DATA_DIR)

if df_torneios.empty:
    st.error("Nenhum torneio encontrado na pasta `torneiosnew/`.")
    st.stop()

# ---------- LÓGICA DA SIDEBAR ----------

# 1. CRIE "ESPAÇOS RESERVADOS" (CONTAINERS) NA ORDEM VISUAL DESEJADA
# O que for criado primeiro aqui, aparecerá mais alto na sidebar.
view_container = st.sidebar.container()
filters_container = st.sidebar.container()

# 2. PREENCHA O CONTAINER DE FILTROS PRIMEIRO (ORDEM LÓGICA)
# Mesmo que ele vá aparecer embaixo, o código dele roda primeiro.
# Isso garante que todas as 'keys' do session_state sejam criadas ANTES de serem usadas.
with filters_container:
    st.header("Filtros de torneios")

    # Definições e valores necessários para os filtros
    tipos_disponiveis = df_torneios["tipo"].dropna().unique().tolist()
    conjuntos_disponiveis = ["Torneios grandes", "Torneios recentes", "Meus favoritos"]
    data_min, data_max = df_torneios["data"].min().date(), df_torneios["data"].max().date()

    # Criação dos widgets de filtro
    tipos_selecionados = st.multiselect(
        "Tipos de torneio",
        options=tipos_disponiveis,
        key="tipos_key"
    )

    conjuntos_selecionados = st.multiselect(
        "Conjuntos de torneios",
        options=conjuntos_disponiveis,
        key="conjuntos_key"
    )

    if "datas_key" not in st.session_state:
        st.session_state["datas_key"] = (data_min, data_max)

    datas = st.date_input(
        "Intervalo de datas",
        min_value=data_min,
        key="datas_key"
    )
    # Pega o valor atual do session_state, que foi atualizado pelo date_input acima
    datas_selecionadas = st.session_state["datas_key"]


    st.button("❌ Limpar tudo", on_click=reset_filtros, args=(df_torneios,), key="limpar_filtros_button")


# Este código roda depois dos filtros, mas o resultado aparece no topo da tela.
with view_container:
    st.header("Selecionar Análise") 
    view_selection = st.radio(
        "**Visualizar**",
        options=['Visão Geral', 'Número de Participantes', 'Detalhes do Torneio', 'Jogadores', 'Tabuleiro de Análise'],
        key='view_key',
        label_visibility="collapsed", # Este parâmetro esconde o rótulo "Selecione uma visualização" da tela
    )

    st.divider()

# ----------------- PÁGINA PRINCIPAL (ÁREA DE CONTEÚDO) ----------------

if len(datas_selecionadas) != 2:
    
    # SE a data estiver incompleta, MOSTRAMOS A PÁGINA DE AVISO
    st.warning("⚠️ **Intervalo de datas incompleto**")
    st.info("Por favor, selecione mais uma data no calendário da barra lateral para exibir os dados.")
    # Você pode até adicionar uma imagem ou um

else:
    # SE a data estiver completa, MOSTRAMOS A PÁGINA NORMAL

    # 4. Com todos os widgets já renderizados, agora é seguro acessar o session_state
    df_filtrado = aplicar_filtros(
        df_torneios,
        tipos=st.session_state["tipos_key"],
        conjuntos=st.session_state["conjuntos_key"],
        datas=st.session_state["datas_key"]
    )


    # ---------- Conteúdo Principal Dinâmico ----------

    # Primeiro, uma verificação geral: se não houver dados, mostre um aviso e pare.
    if df_filtrado.empty:
        st.warning("Nenhum torneio corresponde aos filtros selecionados.")
        st.stop()

    # Agora, use a seleção da sidebar para renderizar a visão correta
    if st.session_state['view_key'] == 'Visão Geral':
        st.subheader("📂 Torneios disponíveis")

        df_ordenado_visao_geral = df_filtrado.copy().sort_values(by="data", ascending=False)
        # Nota: Corrigido de width='stretch' para a opção correta que discutimos
        st.dataframe(df_ordenado_visao_geral, width='stretch')

    elif st.session_state['view_key'] == 'Número de Participantes':
        st.subheader("📈 Total de Jogadores nos Torneios Selecionados")
        # --- CORREÇÃO DAS ESTATÍSTICAS (veja o próximo ponto) ---
        st.write(f"Número de torneios: {len(df_filtrado)}")
        st.write(f"Total de jogos: {df_filtrado['jogos'].sum(skipna=True)}")
        # Corrigindo o rótulo para ser mais honesto
        st.write(f"Total de participações: {df_filtrado['jogadores'].sum(skipna=True)}")
        
        # --- CORREÇÃO DO GRÁFICO ---
        
        # 1. Cria uma cópia ordenada do DataFrame, do mais antigo para o mais recente
        df_grafico = df_filtrado.sort_values(by="data", ascending=True)
        
        # 2. Define a DATA como o índice do gráfico
        df_grafico = df_grafico.set_index("data")

        st.subheader("Jogadores por Torneio (em ordem cronológica)")
        st.bar_chart(df_grafico["jogadores"], width='stretch') # <-- CORRIGIDO
        
        st.subheader("Jogos por Torneio (em ordem cronológica)")
        st.bar_chart(df_grafico["jogos"], use_container_width=True) # <-- CORRIGIDO


    elif st.session_state['view_key'] == 'Detalhes do Torneio':
        st.subheader("🔎 Detalhes de um torneio")

        # Controle de ordenação (renderizado na página principal)
        sort_option = st.radio(
            "Ordenar lista de torneios por:",
            options=["Mais Recentes", "Mais Antigos", "Nome (A-Z)", "Mais Jogadores"],
            horizontal=True,
            key="sort_tournaments_key"
        )        

        # Lógica de ordenação (não visual, apenas prepara os dados)
        if sort_option == 'Mais Recentes':
            df_ordenado = df_filtrado.sort_values(by="data", ascending=False)
        elif sort_option == 'Mais Antigos':
            df_ordenado = df_filtrado.sort_values(by="data", ascending=True)
        elif sort_option == 'Nome (A-Z)':
            df_ordenado = df_filtrado.sort_values(by="nome", ascending=True)
        else: # 'Mais Jogadores'
            df_ordenado = df_filtrado.sort_values(by="jogadores", ascending=False)
        
        st.divider()

        opcao = st.selectbox(
            "Selecione um torneio para ver os detalhes:", 
            df_ordenado["nome"],
            index=None, # Faz com que a seleção inicial seja vazia
            placeholder="Escolha um torneio..."
        )

        if opcao:
            tid = df_ordenado[df_ordenado["nome"] == opcao]["id"].iloc[0]
            paths = torneios[tid]
            info = carregar_info(paths["info"])
            results = carregar_results(paths["results"])
            games = carregar_games(paths["games"])

            st.write(f"### {info.get('name', info.get('fullName', tid))}")
            st.write(f"Tipo: {info.get('system', 'swiss' if 'round' in info else 'desconhecido')}")
            st.write(f"Criado por: {info.get('createdBy')}")
            st.write(f"Número de jogadores: {info.get('nbPlayers')}")
            st.write(f"Número de jogos: {info.get('stats', {}).get('games')}")

            if results:
                results_df = pd.DataFrame(results)
                st.subheader("🏆 Classificação final")
                df_para_exibir = results_df.drop(columns=['flair'], errors='ignore')
                st.dataframe(df_para_exibir, width='stretch')
                if "score" in results_df:
                    st.bar_chart(results_df.set_index("username")["score"])

            if games is not None and not games.empty:
                st.subheader("♟️ Jogos (primeiros 10)")
                st.dataframe(games.head(10), width='stretch')
    elif st.session_state['view_key'] == 'Jogadores':
        st.title("🗂️ Diretório de Jogadores")
        
        # Chama a função que criamos no utils.py
        df_players = carregar_dados_jogadores(PLAYERS_DIR)
        
        if not df_players.empty:
            # --- BARRA LATERAL (FILTROS ESPECÍFICOS DESTA PÁGINA) ---
            st.sidebar.divider()
            st.sidebar.header("Filtros de Jogadores")
            
            # 1. Filtro de Status (Ativo, Banido, Fechado...)
            if "status" in df_players.columns:
                status_unicos = df_players["status"].unique().tolist()
                status_selecionados = st.sidebar.multiselect(
                    "Status da Conta:",
                    options=status_unicos,
                    default=["active"], # Por padrão esconde banidos/inativos
                    format_func=lambda x: x.capitalize()
                )
            else:
                status_selecionados = []
            
            # 2. Busca por Nome
            busca_nome = st.sidebar.text_input("Buscar por nome:", placeholder="Ex: the-chemist")
            
            # 3. Filtro de Participação (Slider)
            max_p = int(df_players["participacoes"].max()) if "participacoes" in df_players.columns else 10
            min_part = st.sidebar.slider("Mínimo de torneios jogados:", 0, max_p, 0)

            # --- APLICANDO OS FILTROS ---
            df_view = df_players.copy()
            
            # Filtra Status
            if status_selecionados:
                df_view = df_view[df_view["status"].isin(status_selecionados)]
                
            # Filtra Nome
            if busca_nome:
                # 'na=False' garante que não quebre se tiver nome vazio
                df_view = df_view[df_view["username"].str.contains(busca_nome, case=False, na=False)]
                
            # Filtra Participações
            if "participacoes" in df_view.columns:
                df_view = df_view[df_view["participacoes"] >= min_part]

            # --- EXIBIÇÃO ---
            
            # Métricas no topo da página
            c1, c2, c3 = st.columns(3)
            c1.metric("Jogadores Listados", len(df_view))
            # c2 e c3 podem ser usados para ratings médios no futuro
            if "participacoes" in df_view.columns:
                 c3.metric("Média de Torneios", f"{df_view['participacoes'].mean():.1f}")

            st.divider()

            # Configuração da Tabela (Beleza Visual)
            st.dataframe(
                df_view,
                column_config={
                    "username": st.column_config.TextColumn(
                        "Jogador",
                        help="Nome de usuário no Lichess"
                    ),
                    "status": st.column_config.SelectboxColumn(
                        "Status",
                        options=["active", "inactive", "closed", "banned"],
                        width="small"
                    ),
                    "participacoes": st.column_config.ProgressColumn(
                        "Torneios Jogados",
                        format="%d",
                        min_value=0,
                        max_value=max_p,
                    ),
                    "last_seen_api_timestamp": st.column_config.DatetimeColumn(
                        "Visto por último",
                        format="D MMM YYYY, HH:mm"
                    ),
                    # Oculta colunas técnicas que não interessam ao usuário
                    "id": None, 
                    "first_seen_team_date": None,
                    "last_seen_team_date": None
                },
                hide_index=True,
                width='stretch',
                height=600
            )
            
        else:
            st.info("Nenhum dado de jogador encontrado. Certifique-se de ter rodado o 'fix_history.py' para popular o banco de dados.")
    elif st.session_state['view_key'] == 'Tabuleiro de Análise':
        st.title("♟️ Console de Análise (Python-Chess)")

        # --- TESTE DO COMPONENTE (temporário) ---

        if "fen" not in st.session_state:
            st.session_state["fen"] = chess.STARTING_FEN

        result = chessboard_component(
            fen=st.session_state["fen"],
            key="analysis_board",
        )

        st.write("Retorno do componente:")
        st.write(result)




        # ===============================
        # ESTADO GLOBAL DO TABULEIRO (FEN)
        # ===============================
        if "fen" not in st.session_state:
            st.session_state["fen"] = chess.STARTING_FEN

        board = chess.Board(st.session_state["fen"])

        # ===============================
        # LAYOUT
        # ===============================
        col_tabuleiro, col_controles = st.columns([1.5, 1])

        # ===============================
        # TABULEIRO (SVG TEMPORÁRIO)
        # ===============================
        with col_tabuleiro:
            boardsvg = chess.svg.board(board=board, size=600)
            b64 = base64.b64encode(boardsvg.encode("utf-8")).decode("utf-8")
            st.markdown(
                f'<img src="data:image/svg+xml;base64,{b64}" width="100%"/>',
                unsafe_allow_html=True
            )

        # ===============================
        # CONTROLES
        # ===============================
        with col_controles:
            st.subheader("Controles")

            # -------------------------------
            # DESFAZER
            # -------------------------------
            if st.button("⬅️ Desfazer"):
                if board.move_stack:
                    board.pop()
                    st.session_state["fen"] = board.fen()
                    st.rerun()

            # -------------------------------
            # RESET
            # -------------------------------
            if st.button("🔄 Reiniciar"):
                st.session_state["fen"] = chess.STARTING_FEN
                st.rerun()

            st.divider()

            # -------------------------------
            # DEBUG / INFORMAÇÕES TÉCNICAS
            # -------------------------------
            st.caption("Estado Técnico (FEN):")
            st.code(board.fen(), language="text")

            if board.is_check():
                st.warning("⚠️ O rei está em XEQUE!")
            if board.is_checkmate():
                st.error("🏆 XEQUE-MATE!")
            if board.is_stalemate():
                st.info("½ - ½ AFOGAMENTO (Empate)")

            if board.move_stack:
                st.text(f"Último lance: {board.peek()}")
