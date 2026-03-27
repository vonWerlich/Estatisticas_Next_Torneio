import streamlit as st

def renderizar_aba_home():
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