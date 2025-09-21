import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
from streamlit_elements import elements, mui, dashboard
from contextlib import contextmanager # Importação chave

@contextmanager
def caixa_redimensionavel(titulo, key_painel):
    layout = [
        dashboard.Item(f"item_{key_painel}", 0, 0, 12, 8, isResizable=True, isDraggable=True),
    ]
    # Cria o container invisível
    with elements(key_painel):
        st.markdown(f"""
        <style>
        div[id="{key_painel}"] > div:first-child {{
            display:none;  /* oculta a div extra */
        }}
        </style>
        """, unsafe_allow_html=True)
        
        with dashboard.Grid(layout):
            with mui.Card(sx={"display": "flex", "flexDirection": "column"}):
                mui.CardHeader(title=titulo)
                with mui.CardContent(sx={"flex": 1, "minHeight": 0}):
                    yield

def mostrar_torneios_filtrados(df):
    """
    Exibe a tabela de torneios com AgGrid (versão flexível).
    """
    if df.empty:
        st.warning("Nenhum torneio corresponde aos filtros selecionados.")
        return
    
    
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(resizable=True)
    gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=15)
    gb.configure_grid_options(domLayout='normal')
    grid_options = gb.build()

    AgGrid(
            df,
            gridOptions=grid_options,
            height='100%',
            width='100%',
            theme='streamlit',
            fit_columns_on_grid_load=True,
            reload_data=True,
            key='torneios_grid_resizable'
    )

__all__ = ["mostrar_torneios_filtrados", "caixa_redimensionavel"]