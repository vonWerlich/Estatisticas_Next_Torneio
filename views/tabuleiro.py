import streamlit as st
import chess
import chess.svg
import base64

try:
    from chessboard_component import chessboard_component
except ImportError:
    chessboard_component = None

def renderizar_aba_tabuleiro():
    st.subheader("Tabuleiro de Análise")

    if "fen" not in st.session_state:
        st.session_state["fen"] = chess.STARTING_FEN

    if chessboard_component:
        try:
            # O FEN retornado pelo componente NÃO deve ser salvo no st.session_state["fen"].
            # Isso é proposital. O comportamento esperado é que o tabuleiro seja efêmero 
            # e resete para a posição inicial (ou a selecionada nos filtros) a cada reload.
            # NÃO é preciso atualizar o st.session_state aqui.
            move_data = chessboard_component(fen=st.session_state["fen"], key="analysis_board")
            if move_data:
                pass
        except Exception:
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