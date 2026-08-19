import streamlit as st
import chess
import chess.svg
import base64
import os
from libsql_client import create_client_sync

try:
    from chessboard_component import chessboard_component
except ImportError:
    chessboard_component = None

@st.cache_data(ttl=3600, show_spinner=False)
def buscar_dados_explorador(fen_completo):
    fen_base = " ".join(fen_completo.split(" ")[:4])
    turso_url = os.environ.get("TURSO_URL")
    turso_token = os.environ.get("TURSO_TOKEN")
    
    if not turso_url or not turso_token:
        return {"moves": [], "games": []}
    
    try:
        client = create_client_sync(url=turso_url, auth_token=turso_token)
        
        # Query 1: Top Lances com contagem de vitórias/empates/derrotas
        query_moves = """
            SELECT o.lance_jogado, COUNT(o.id_partida) as jogos,
                   AVG(p.rating_brancas) as avg_w, AVG(p.rating_negras) as avg_b,
                   SUM(CASE WHEN p.resultado = '1-0' THEN 1 ELSE 0 END) as w_wins,
                   SUM(CASE WHEN p.resultado = '1/2-1/2' THEN 1 ELSE 0 END) as draws,
                   SUM(CASE WHEN p.resultado = '0-1' THEN 1 ELSE 0 END) as b_wins
            FROM ocorrencias o
            JOIN partidas p ON o.id_partida = p.id
            JOIN posicoes pos ON o.id_posicao = pos.id
            WHERE pos.fen_base = ? AND o.lance_jogado IS NOT NULL
            GROUP BY o.lance_jogado
            ORDER BY jogos DESC
            LIMIT 10
        """
        res_moves = client.execute(query_moves, [fen_base])
        
        # Query 2: Top Partidas naquela posição
        # AQUI FOI ADICIONADO 'o.lance_jogado' no SELECT
        query_games = """
            SELECT p.id, p.brancas, p.negras, p.rating_brancas, p.rating_negras, p.resultado, p.data, o.lance_jogado
            FROM ocorrencias o
            JOIN partidas p ON o.id_partida = p.id
            JOIN posicoes pos ON o.id_posicao = pos.id
            WHERE pos.fen_base = ?
            GROUP BY p.id
            ORDER BY (p.rating_brancas + p.rating_negras) DESC
            LIMIT 10
        """
        res_games = client.execute(query_games, [fen_base])
        client.close()
        
        moves = [{
            "san": row[0], "games": int(row[1]),
            "white_elo": float(row[2]), "black_elo": float(row[3]),
            "w_wins": int(row[4]), "draws": int(row[5]), "b_wins": int(row[6])
        } for row in res_moves.rows]
        
        games = [{
            "id": row[0], "white": row[1], "black": row[2],
            "white_elo": int(row[3]), "black_elo": int(row[4]),
            "result": row[5], "date": row[6],
            "move": row[7] # AQUI O LANCE É ADICIONADO AO OBJETO GAME
        } for row in res_games.rows]
        
        return {"moves": moves, "games": games}
        
    except Exception as e:
        print(f"❌ Erro ao consultar Turso: {e}")
        return {"moves": [], "games": []}

def renderizar_aba_tabuleiro():
    st.subheader("Tabuleiro de Análise")

    if "fen" not in st.session_state:
        st.session_state["fen"] = chess.STARTING_FEN

    if chessboard_component:
        try:
            # 1. Busca os dados super enriquecidos
            explorer_data = buscar_dados_explorador(st.session_state["fen"])
            
            # 2. Injeta FEN e Dados no React usando a nova prop
            move_data = chessboard_component(
                fen=st.session_state["fen"], 
                explorer_data=explorer_data,
                key="analysis_board"
            )
            
            if move_data and "fen" in move_data and move_data["fen"] != st.session_state["fen"]:
                st.session_state["fen"] = move_data["fen"]
                st.rerun()

        except Exception as e:
            st.error(f"Erro no componente: {e}")
            _renderizar_tabuleiro_estatico()
    else:
        st.warning("Componente 'chessboard_component' não encontrado. Usando visualização estática.")
        _renderizar_tabuleiro_estatico()

def _renderizar_tabuleiro_estatico():
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