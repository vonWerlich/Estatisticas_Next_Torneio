import streamlit as st
import pandas as pd
from utils import *
from filters import *
from visualizations import *
from components import *
from layout import *
from pathlib import Path

DATA_DIR = "torneiosnew"  # pasta onde estão todos os torneios

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

@st.cache_data(ttl="4d") # <-- cache para atualização mais rápida, dura 4 dias
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

with st.spinner("Aguarde, preparando as estatísticas de todos os torneios... 🏋️‍♂️"):
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
        options=['Visão Geral', 'Estatísticas', 'Detalhes do Torneio'],
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
        # Nota: Corrigido de width='stretch' para a opção correta que discutimos
        st.dataframe(df_filtrado.copy(), width='stretch')

    elif st.session_state['view_key'] == 'Estatísticas':
        st.subheader("📈 Estatísticas dos torneios selecionados")
        st.write(f"Número de torneios: {len(df_filtrado)}")
        st.write(f"Total de jogos: {df_filtrado['jogos'].sum(skipna=True)}")
        st.write(f"Total de jogadores (soma): {df_filtrado['jogadores'].sum(skipna=True)}")
        st.bar_chart(df_filtrado.set_index("nome")["jogos"])

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
            df_filtrado["nome"],
            index=None, # Faz com que a seleção inicial seja vazia
            placeholder="Escolha um torneio..."
        )

        if opcao:
            tid = df_filtrado[df_filtrado["nome"] == opcao]["id"].iloc[0]
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
                st.dataframe(results_df, use_container_width=True)
                if "score" in results_df:
                    st.bar_chart(results_df.set_index("username")["score"])

            if games is not None and not games.empty:
                st.subheader("♟️ Jogos (primeiros 10)")
                st.dataframe(games.head(10), use_container_width=True)
