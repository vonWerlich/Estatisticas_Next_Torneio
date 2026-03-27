import streamlit as st
from utils import carregar_numero_participantes_total_unico, carregar_detalhes_torneio_sql, carregar_games_ndjson

def renderizar_aba_torneios(df_filtrado):
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
            df_jogadores = carregar_numero_participantes_total_unico()
            df_stats = df_jogadores[df_jogadores['tournament_id'].isin(df_filtrado['id'])]

            c1, c2, c3 = st.columns(3)
            c1.metric("Torneios Filtrados", len(df_filtrado))
            c2.metric("Total de Participações", len(df_stats)) 
            c3.metric("Jogadores Únicos", df_stats['user_id_lichess'].nunique()) 

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