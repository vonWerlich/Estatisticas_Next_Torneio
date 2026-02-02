import React from "react";
import { createRoot } from "react-dom/client";
import { Streamlit, RenderData } from "streamlit-component-lib";
import MyComponent from "./MyComponent";

// Encontra o container
const container = document.querySelector(".react-root");
if (!container) throw new Error("Erro: A div .react-root não foi encontrada no HTML");

const root = createRoot(container);

// Função chamada toda vez que o Streamlit envia novos dados
const onRender = (event: Event) => {
  const data = (event as CustomEvent<RenderData>).detail;

  // Pegue os argumentos que vêm do Python
  const { fen, orientation } = data.args;

  root.render(
    <React.StrictMode>
      <MyComponent 
        fen={fen ?? "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"}  // fallback padrão
        orientation={orientation}  // pode ser "white" | "black" ou undefined
      />
    </React.StrictMode>
  );

  // Ajusta a altura do iframe automaticamente
  Streamlit.setFrameHeight();
};

// Registra o listener de render
Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender);

// Informa ao Streamlit que o componente está pronto
Streamlit.setComponentReady();

// Altura inicial
Streamlit.setFrameHeight();