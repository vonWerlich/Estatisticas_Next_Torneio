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

# ---------- Sidebar: filtros ----------
st.sidebar.header("Filtros de torneios")

tipos_disponiveis = df_torneios["tipo"].dropna().unique().tolist()
conjuntos_disponiveis = ["Torneios grandes", "Torneios recentes", "Meus favoritos"]


# ----- Valores iniciais de datas -----
data_min, data_max = df_torneios["data"].min().date(), df_torneios["data"].max().date()


# ----- Multiselects com keys (sem default) -----
tipos_selecionados = st.sidebar.multiselect(
    "Tipos de torneio",
    options=tipos_disponiveis,
    key="tipos_key"
)

conjuntos_selecionados = st.sidebar.multiselect(
    "Conjuntos de torneios",
    options=conjuntos_disponiveis,
    key="conjuntos_key"
)

# ----- Intervalo de datas -----
# Inicializa session_state se não existir
if "datas_key" not in st.session_state:
    st.session_state["datas_key"] = (data_min, data_max)

# Intervalo de datas usando session_state como valor inicial
datas = st.sidebar.date_input(
    "Intervalo de datas",
    min_value=data_min,
    # max_value=data_max, # se estiver ativo, não deixa colocar datas posteriores ao ultimo torneio
    key="datas_key"
)

#  Botão Clear 
st.sidebar.button("❌ Limpar tudo", on_click=reset_filtros, args=(df_torneios,), key="limpar_filtros_button")

# Adiciona um separador visual
st.sidebar.divider() 

# NOVO: Seletor de qual visualização mostrar na página principal
view_selection = st.sidebar.radio(
    "**Visualizar**",
    options=['Visão Geral', 'Estatísticas', 'Detalhes do Torneio'],
    key='view_key'
)

# ---------- Aplicar filtros ----------
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
