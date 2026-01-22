import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path

_component = components.declare_component(
    "chessboard_component",
    path=str(Path(__file__).parent / "frontend" / "build"),
)

def chessboard_component(fen: str, key=None):
    """
    Componente de tabuleiro de xadrez interativo.

    Parameters
    ----------
    fen : str
        Posição atual do tabuleiro em FEN.
    key : str or None
        Chave opcional do Streamlit.

    Returns
    -------
    dict | None
        {"uci_move": "e2e4"} ou {"uci_move": None}
    """
    return _component(
        fen=fen,
        key=key,
        default={"uci_move": None},
    )
