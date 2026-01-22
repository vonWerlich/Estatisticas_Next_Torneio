import React from "react";
import { createRoot } from "react-dom/client";
import { Streamlit, RenderData } from "streamlit-component-lib";
import MyComponent from "./MyComponent";

// 1. Encontra onde desenhar
const container = document.querySelector(".react-root");
if (!container) throw new Error("Erro: A div .react-root não foi encontrada no HTML");

const root = createRoot(container);

// 2. Função que roda toda vez que o Python fala com o componente
const onRender = (event: Event) => {
  const data = (event as CustomEvent<RenderData>).detail;
  
  // Pega os dados vindos do Python (ex: fen)
  // O "args" contém os argumentos passados no declare_component
  const fen = data.args.fen;

  // 3. Desenha o componente
  root.render(
    <React.StrictMode>
      <MyComponent 
        fen={fen} 
        setStateValue={(key, value) => {
            // Essa função conecta o React de volta ao Python
            // Se o MyComponent pedir setStateValue("uci_move", "e2e4")...
            // ...nós avisamos o Streamlit.
            Streamlit.setComponentValue({ [key]: value });
        }}
      />
    </React.StrictMode>
  );
  
  // Avisa o Streamlit que terminamos de desenhar e ajusta a altura
  Streamlit.setFrameHeight();
};

// Conecta os ouvidos ao Streamlit
Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender);

// Avisa que estamos prontos para receber dados
Streamlit.setComponentReady();
// Ajusta a altura inicial (caso o render demore)
Streamlit.setFrameHeight();