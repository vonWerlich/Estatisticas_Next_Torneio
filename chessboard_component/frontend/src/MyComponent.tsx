import { FC, ReactElement, useEffect, useLayoutEffect, useRef } from "react";
import { Chessground } from "chessground";
import type { Api } from "chessground/api";
import type { Config } from "chessground/config";
import { Streamlit } from "streamlit-component-lib";

import "chessground/assets/chessground.base.css";
import "chessground/assets/chessground.cburnett.css"; 

interface MyComponentProps {
  fen: string;
  setStateValue: (key: string, value: any) => void;
}

const MyComponent: FC<MyComponentProps> = ({ fen, setStateValue }): ReactElement => {
  const boardRef = useRef<HTMLDivElement | null>(null);
  const containerRef = useRef<HTMLDivElement | null>(null);
  const apiRef = useRef<Api | null>(null);

  // 1. ESTILO MATEMÁTICO (CSS PURO)
  // Em vez de carregar uma imagem que pode distorcer, instruímos o navegador
  // a desenhar os quadrados usando gradientes.
  useLayoutEffect(() => {
    const css = `
      /* ALVO: O tabuleiro */
      cg-board {
        /* CORES EXATAS DO LICHESS BROWN */
        /* Usa gradiente cônico para criar 4 quadrados (2 claros, 2 escuros) */
        background-image: conic-gradient(
          #b58863 90deg, 
          #f0d9b5 90deg 180deg, 
          #b58863 180deg 270deg, 
          #f0d9b5 270deg
        ) !important;
        
        /* MATEMÁTICA DO TAMANHO: 
           O tabuleiro tem 8x8 casas. 
           O padrão acima cria um bloco de 2x2 casas.
           Portanto, precisamos que esse bloco se repita 4 vezes (100% / 4 = 25%).
        */
        background-size: 25% 25% !important;
        
        /* Remove qualquer imagem antiga ou cor de fundo que atrapalhe */
        background-color: #f0d9b5 !important;
      }

      /* Cores de destaque (Movimentos, Seleção, Check) */
      cg-board square.move-dest { background: radial-gradient(rgba(20, 85, 30, 0.5) 22%, #208530 0, rgba(0, 0, 0, 0.3) 0, rgba(0, 0, 0, 0) 0) !important; }
      cg-board square.premove-dest { background: radial-gradient(rgba(20, 30, 85, 0.5) 22%, #203085 0, rgba(0, 0, 0, 0.3) 0, rgba(0, 0, 0, 0) 0) !important; }
      cg-board square.oc.move-dest { background: radial-gradient(transparent 0%, transparent 80%, rgba(20, 85, 0, 0.3) 80%) !important; }
      cg-board square.oc.premove-dest { background: radial-gradient(transparent 0%, transparent 80%, rgba(20, 30, 85, 0.2) 80%) !important; }
      cg-board square.move-dest:hover { background: rgba(20, 85, 30, 0.3) !important; }
      cg-board square.premove-dest:hover { background: rgba(20, 30, 85, 0.2) !important; }
      cg-board square.last-move { background-color: rgba(155, 199, 0, 0.41) !important; }
      cg-board square.selected { background-color: rgba(20, 85, 30, 0.5) !important; }
      cg-board square.check { background: radial-gradient(ellipse at center, rgba(255, 0, 0, 1) 0%, rgba(231, 0, 0, 1) 25%, rgba(169, 0, 0, 0) 89%, rgba(158, 0, 0, 0) 100%) !important; }
      
      /* Coordenadas visíveis */
      .orientation-white .ranks :nth-child(odd), .orientation-white .files :nth-child(even),
      .orientation-black .ranks :nth-child(even), .orientation-black .files :nth-child(odd) { color: #f0d9b5 !important; } /* Cor clara nas casas escuras */
      
      .orientation-white .ranks :nth-child(even), .orientation-white .files :nth-child(odd),
      .orientation-black .ranks :nth-child(odd), .orientation-black .files :nth-child(even) { color: #b58863 !important; } /* Cor escura nas casas claras */
    `;

    const styleEl = document.createElement('style');
    styleEl.innerHTML = css;
    document.head.appendChild(styleEl);

    return () => {
      if (document.head.contains(styleEl)) {
        document.head.removeChild(styleEl);
      }
    };
  }, []);

  // 2. VIGIA DE RESIZE
  useEffect(() => {
    if (!containerRef.current) return;
    const resizeObserver = new ResizeObserver(() => {
      Streamlit.setFrameHeight();
      apiRef.current?.redrawAll();
    });
    resizeObserver.observe(containerRef.current);
    return () => resizeObserver.disconnect();
  }, []);

  // 3. INICIALIZAÇÃO
  useEffect(() => {
    if (!boardRef.current) return;

    const config: Config = {
      fen: fen,
      orientation: "white",
      movable: {
        free: false,
        color: "both",
        events: {
          after: (orig, dest) => {
            const uci = `${orig}${dest}`;
            setStateValue("uci_move", uci);
          },
        },
      },
      animation: { enabled: true, duration: 200 },
    };

    apiRef.current = Chessground(boardRef.current, config);

    // --- GARANTIA EXTRA ---
    // Remove qualquer background inline que a biblioteca tente colocar
    setTimeout(() => {
       const boardEl = boardRef.current?.querySelector('cg-board') as HTMLElement;
       if (boardEl) {
           // Limpamos a imagem para garantir que o CSS Gradient assuma
           boardEl.style.backgroundImage = ''; 
       }
    }, 50);

    return () => {
      apiRef.current?.destroy();
      apiRef.current = null;
    };
  }, []);

  // 4. ATUALIZAÇÃO FEN
  useEffect(() => {
    apiRef.current?.set({ fen: fen });
  }, [fen]);

  return (
    <div style={{ display: 'flex', justifyContent: 'center', paddingBottom: '10px' }}>
      <div 
        ref={containerRef}
        style={{ 
          position: 'relative',
          width: '500px',     
          maxWidth: '100%',   
          aspectRatio: '1 / 1', 
          resize: 'horizontal', 
          overflow: 'hidden',   
          border: '1px solid #dcdcdc',
          borderRadius: '4px',
          boxShadow: '0 4px 6px rgba(0,0,0,0.1)'
        }}
      >
        <div
          ref={boardRef}
          style={{ width: "100%", height: "100%" }}
        />
      </div>
    </div>
  );
};

export default MyComponent;