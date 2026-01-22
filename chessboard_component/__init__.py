import streamlit.components.v1 as components
from pathlib import Path

# Garante o caminho absoluto e resolve problemas de barra do Windows
frontend_dir = (Path(__file__).parent / "frontend" / "build").resolve()

# Debug no terminal para termos certeza
if not frontend_dir.exists():
    print(f"❌ ERRO: Pasta não encontrada: {frontend_dir}")
elif not (frontend_dir / "index.html").exists():
    print(f"❌ ERRO: index.html não encontrado em: {frontend_dir}")
else:
    print(f"✅ SUCESSO: Carregando componente de: {frontend_dir}")

_component = components.declare_component(
    "chessboard_component",
    path=str(frontend_dir)
)

def chessboard_component(fen: str, key=None):
    return _component(
        fen=fen,
        key=key,
        default={"uci_move": None},
    )