import streamlit as st
import streamlit.components.v1 as components

def ajustar_layout_principal(padding_top_rem=0, margin_top_rem=-3):
    """
    Ajusta o padding e a margem do container principal para
    compensar a altura do header customizado.
    """
    st.markdown(
        f"""
        <style>
        .block-container {{
            padding-top: {padding_top_rem}rem;
            margin-top: {margin_top_rem}rem; /* Puxa o conteúdo para cima */
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

### não está mais sendo usada, substituída por css
def adicionar_titulo_no_header(titulo_html: str):
    """
    Usa a API de componentes para injetar o header.
    Esta é uma abordagem mais robusta que o st.markdown.
    """
    # Combinamos o HTML, CSS e JavaScript em uma única string
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <script>
        // Função para injetar o header no documento pai
        function injectHeaderInParent() {{
            console.log('COMPONENTE: Tentando injetar header no pai...');
            const header = window.parent.document.querySelector('header[data-testid="stHeader"]');
            
            if (header) {{
                console.log('COMPONENTE: Header do pai encontrado!');
                if (!header.querySelector('#custom-header-title')) {{
                    const customTitle = document.createElement('div');
                    customTitle.id = 'custom-header-title';
                    customTitle.innerHTML = `{titulo_html}`;
                    header.prepend(customTitle);
                    console.log('COMPONENTE: Título injetado com sucesso!');
                }}
                return true;
            }}
            return false;
        }}

        // Tenta repetidamente até conseguir
        const intervalId = setInterval(() => {{
            if (injectHeaderInParent()) {{
                clearInterval(intervalId);
            }}
        }}, 250);

        // Para de tentar após 5 segundos
        setTimeout(() => {{ clearInterval(intervalId); }}, 5000);
    </script>
    </head>
    <body>
    </body>
    </html>
    """
    # Renderiza o HTML em um componente de altura zero para que ele não ocupe espaço
    components.html(html_content, height=0)

def aplicar_estilos_globais(logo_base64: str):
    """
    Aplica todos os estilos CSS customizados à aplicação Streamlit.
    """
    # 1. Estilos para o Header da Sidebar (com a logo)
    st.markdown(
        f"""
        <style>
            [data-testid="stSidebarHeader"] {{
                background-image: url("data:image/png;base64,{logo_base64}");
                background-repeat: no-repeat;
                background-size: contain;
                background-position: 20px center;
                background-size: 170px;
                padding-left: 120px;
                min-height: 140px;
                padding-top: 10px;
                padding-bottom: 10px;
                border-bottom: 2px solid #3a3f4e;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    # 2. Estilos para o Header Principal (com o título)
    st.markdown(
        """
        <style>
            header[data-testid="stHeader"] {
                align-items: center;
            }

            header[data-testid="stHeader"]::before {
                content: "Análise de Dados dos Torneios do NEXT";
                font-family: 'Source Sans Pro', sans-serif;
                font-size: 28px;
                font-weight: 600;
                color: var(--text-color);
                margin-left: 20px;
                margin-right: auto;
                white-space: nowrap;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

__all__ = ["ajustar_layout_principal", "aplicar_estilos_globais"]