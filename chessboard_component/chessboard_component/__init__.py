import streamlit as st
from pathlib import Path

_component_func = st.components.v2.component(
    "chessboard_component.chessboard_component",
    path=str(
        Path(__file__).parent / "frontend" / "build"
    ),
)


def chessboard_component(fen, key=None):
    return _component_func(
        fen=fen,
        key=key,
        default={"uci_move": None},
    )
