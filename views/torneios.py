import streamlit as st
from utils import *

def renderizar_aba_torneios(df_filtrado):
    sub_aba = st.radio(
        "Navegação Interna:", 
        ["🏆 Painel de Vencedores", "📂 Visão Geral", "📈 Estatísticas", "🔎 Detalhes"], 
        horizontal=True,
        label_visibility="collapsed"
    )
    st.markdown('<hr style="margin-top: -15px; margin-bottom: 15px; border: 0; border-top: 1px solid #808080; opacity: 0.5;">', unsafe_allow_html=True)
    
    if sub_aba == "🏆 Painel de Vencedores":
        st.subheader("Painel de Vencedores")
        
        if not df_filtrado.empty:
            df_resultados = carregar_pontuacoes_vencedores(df_filtrado['id'].tolist())
            
            if not df_resultados.empty:
                # ---- CONTROLES SUPERIORES LADO A LADO ----
                col_sistema, col_extras = st.columns(2)
                
                with col_sistema:
                    sistema = st.selectbox(
                        "Sistema de Pontuação:",
                        [
                            "NEXT (Padrão 10 a 1)", 
                            "Fórmula 1 (Atual: 25-18-15...)", 
                            "F1 Clássica (Top 6: 10-6-4...)", 
                            "Pódio Apenas (3-2-1)"
                        ]
                    )
                
                with col_extras:
                    # Injeta um espaço em branco com a altura exata da legenda do selectbox
                    st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
                    with st.expander("⚙️ Curiosidades e Colunas Extras"):
                        posicoes_extras = st.number_input("Mostrar contagem de posições até o:", min_value=3, max_value=50, value=10, step=1)
                        mostrar_lanternas = st.checkbox("Mostrar contagem de 'Lanternas' (Último lugar do torneio)", value=False)
                
                # Chamada da nossa nova função do utils.py
                df_ranking = gerar_ranking_vencedores(df_resultados, sistema, posicoes_extras, mostrar_lanternas)
                
                if not df_ranking.empty:
                    # Configuração visual das colunas
                    col_config = {
                        "username": "Jogador",
                        "pontos": st.column_config.NumberColumn("Pontos", format="%d")
                    }
                    
                    for i in range(1, posicoes_extras + 1):
                        if i == 1: label = "🥇 1º"
                        elif i == 2: label = "🥈 2º"
                        elif i == 3: label = "🥉 3º"
                        else: label = f"{i}º"
                        col_config[f"{i}º"] = st.column_config.NumberColumn(label, format="%d")
                        
                    if mostrar_lanternas:
                        col_config["🐢 Lanterna"] = st.column_config.NumberColumn("🐢 Últimos", format="%d")
                    
                    st.dataframe(
                        df_ranking, 
                        hide_index=True, 
                        width='stretch',
                        column_config=col_config
                    )
                else:
                    st.warning("Ninguém pontuou sob este sistema nos torneios selecionados.")
            else:
                st.warning("Nenhum resultado processado para os torneios exibidos.")
        else:
            st.info("Nenhum torneio válido para gerar o painel.")
            
            
    elif sub_aba == "📂 Visão Geral":
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