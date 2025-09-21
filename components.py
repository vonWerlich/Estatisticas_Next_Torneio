import streamlit as st

def slider_altura():
    return st.slider("Altura da tabela (px)", 200, 1000, 400)

def slider_largura():
    return st.slider("Largura da tabela (px)", 400, 1200, 800)

def slider_largura_porcentagem_da_tela():
    return st.slider("Ajuste da largura da área principal (%)", 50, 100, 80)

#função para resetar filtros
def reset_filtros(df):
    st.session_state["tipos_key"] = []
    st.session_state["conjuntos_key"] = []
    st.session_state["datas_key"] = (df["data"].min().date(), df["data"].max().date())

__all__ = ["slider_altura", "slider_largura", "reset_filtros",
           "slider_largura_porcentagem_da_tela"]

