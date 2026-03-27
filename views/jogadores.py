import streamlit as st
import pandas as pd
from utils import carregar_dados_jogadores_sql, carregar_numero_participantes_total_unico

def renderizar_aba_jogadores(df_filtrado):
    st.subheader("Diretório de Jogadores")
    
    df_players_all = carregar_dados_jogadores_sql()
    
    if not df_players_all.empty and not df_filtrado.empty:
        df_participacoes = carregar_numero_participantes_total_unico()
        participacoes_filtradas = df_participacoes[df_participacoes['tournament_id'].isin(df_filtrado['id'])]
        jogadores_no_filtro = participacoes_filtradas['user_id_lichess'].unique()
        df_players = df_players_all[df_players_all['username'].isin(jogadores_no_filtro)].copy()
        
        contagem_filtrada = participacoes_filtradas.groupby('user_id_lichess').size().reset_index(name='part_filtradas')
        df_players = df_players.merge(contagem_filtrada, left_on='username', right_on='user_id_lichess', how='left')
        df_players['participacoes'] = df_players['part_filtradas'].fillna(0).astype(int)
        df_players = df_players.drop(columns=['part_filtradas'])
        
    else:
        df_players = pd.DataFrame()

    if not df_players.empty:
        with st.sidebar:
            st.divider()
            st.markdown("### 👤 Filtros de Jogadores")
            
            opcoes_status = df_players["status"].unique().tolist() if "status" in df_players.columns else ["active"]
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
            "username", "status", "last_seen_api_timestamp",
            "rating_blitz", "rating_rapid", "rating_chess960", "participacoes"
        ]

        st.dataframe(
            df_view,
            column_order=colunas_exibidas,
            column_config={
                "username": st.column_config.TextColumn("Jogador", help="ID Lichess"),
                "status": st.column_config.SelectboxColumn("Status", width="small", options=opcoes_status),
                "participacoes": st.column_config.ProgressColumn("Torneios", format="%d", min_value=0, max_value=max_p),
                "rating_blitz": st.column_config.NumberColumn("Blitz", format="%d", help="Rating Blitz"),
                "rating_rapid": st.column_config.NumberColumn("Rapid", format="%d", help="Rating Rápidas"),
                "rating_chess960": st.column_config.NumberColumn("Chess 960", format="%d", help="Rating Xadrez 960"),
                "rating_classical": st.column_config.NumberColumn("Classical", format="%d", help="Rating Clássicas"),
                "rating_bullet": st.column_config.NumberColumn("Bullet", format="%d", help="Rating Bullet"),
                "last_seen_api_timestamp": st.column_config.DatetimeColumn("Visto por último", format="D MMM YYYY", help="Última data no Lichess"),
            },
            hide_index=True, width='stretch', height=600
        )
    else:
        st.info("Nenhum jogador encontrado no banco de dados.")