import { FC, ReactElement, useEffect, useLayoutEffect, useRef } from "react";
import { Chessground } from "chessground";
import type { Api } from "chessground/api";
import type { Config } from "chessground/config";
import { Key } from "chessground/types";
import { Streamlit } from "streamlit-component-lib";
import { Chess } from "chess.js";

import "chessground/assets/chessground.base.css";
import "chessground/assets/chessground.cburnett.css"; 

interface MyComponentProps {
  fen: string;
  orientation?: "white" | "black";
  setStateValue: (key: string, value: any) => void;
}

// --- SONS (Mantidos, caso você queira usar depois) ---
const SOUNDS = {
  move: new Audio("https://raw.githubusercontent.com/lichess-org/lila/master/public/sound/standard/Move.mp3"),
  capture: new Audio("https://raw.githubusercontent.com/lichess-org/lila/master/public/sound/standard/Capture.mp3"),
  check: new Audio("https://raw.githubusercontent.com/lichess-org/lila/master/public/sound/standard/Check.wav"),
};
// Tenta pré-carregar sem travar se falhar
try { Object.values(SOUNDS).forEach(s => s.load()); } catch(e) {}


function toDests(chess: Chess): Map<Key, Key[]> {
  const dests = new Map();
  chess.moves({ verbose: true }).forEach((m) => {
    if (!dests.has(m.from)) dests.set(m.from, []);
    dests.get(m.from).push(m.to);
  });
  return dests;
}

const MyComponent: FC<MyComponentProps> = ({ fen, orientation = "white", setStateValue }): ReactElement => {
  const boardRef = useRef<HTMLDivElement | null>(null);
  const containerRef = useRef<HTMLDivElement | null>(null);
  const apiRef = useRef<Api | null>(null);
  const chessRef = useRef(new Chess(fen));

  // --- CSS REFINADO (ESTILO LICHESS "MOLDURA") ---
  useLayoutEffect(() => {
    const css = `
      /* Tabuleiro Matemático (Madeira) */
      cg-board {
        background-image: conic-gradient(
          #b58863 90deg, #f0d9b5 90deg 180deg, 
          #b58863 180deg 270deg, #f0d9b5 270deg
        ) !important;
        background-size: 25% 25% !important;
        background-color: #f0d9b5 !important;
      }
      
      /* 1. BOLINHA (Casa Vazia) - Mantém o padrão Lichess */
      cg-board square.move-dest { 
        background: radial-gradient(rgba(20, 85, 30, 0.5) 19%, rgba(0, 0, 0, 0) 20%) !important; 
      }

      /* 2. MOLDURA DE CAPTURA (Casa Ocupada - .oc) - A MUDANÇA ESTÁ AQUI */
      /* Usamos 4 gradientes lineares, um para cada canto, criando triângulos */
      cg-board square.oc.move-dest { 
        background-image: 
            /* Canto Superior Esquerdo */
            linear-gradient(to bottom right, rgba(20, 85, 30, 0.6) 15%, transparent 15%),
            /* Canto Superior Direito */
            linear-gradient(to bottom left, rgba(20, 85, 30, 0.6) 15%, transparent 15%),
            /* Canto Inferior Esquerdo */
            linear-gradient(to top right, rgba(20, 85, 30, 0.6) 15%, transparent 15%),
            /* Canto Inferior Direito */
            linear-gradient(to top left, rgba(20, 85, 30, 0.6) 15%, transparent 15%) !important;
        /* O '15%' define o tamanho do triângulo. Aumente para triângulos maiores. */
      }

      /* Hover, Seleção e Xeque */
      cg-board square.move-dest:hover { background: rgba(20, 85, 30, 0.3) !important; }
      cg-board square.last-move { background-color: rgba(155, 199, 0, 0.41) !important; }
      cg-board square.selected { background-color: rgba(20, 85, 30, 0.5) !important; }
      cg-board square.check { background: radial-gradient(ellipse at center, rgba(255, 0, 0, 1) 0%, rgba(231, 0, 0, 1) 25%, rgba(169, 0, 0, 0) 89%, rgba(158, 0, 0, 0) 100%) !important; }
      
      /* Coordenadas */
      .orientation-white .ranks :nth-child(odd), .orientation-white .files :nth-child(even),
      .orientation-black .ranks :nth-child(even), .orientation-black .files :nth-child(odd) { color: #f0d9b5 !important; }
      .orientation-white .ranks :nth-child(even), .orientation-white .files :nth-child(odd),
      .orientation-black .ranks :nth-child(odd), .orientation-black .files :nth-child(even) { color: #b58863 !important; }
    `;
    const styleEl = document.createElement('style');
    styleEl.innerHTML = css;
    document.head.appendChild(styleEl);
    return () => { if (document.head.contains(styleEl)) document.head.removeChild(styleEl); };
  }, []);

  // --- LÓGICA DO JOGO (Mantida igual) ---
  useEffect(() => {
    if (!boardRef.current) return;
    const chess = chessRef.current;
    try { chess.load(fen); } catch (e) { }

    const config: Config = {
      fen: fen,
      orientation: orientation,
      movable: {
        free: false,
        color: "both",
        dests: toDests(chess),
        showDests: true,
        events: {
          after: (orig, dest) => {
            // Lógica de movimento e som
            const moveAttempt = { from: orig, to: dest, promotion: 'q' };
            const move = chess.move(moveAttempt); 
            
            if (move) {
                // Toca os sons (se os arquivos carregaram)
                try {
                  if (chess.isCheck() || chess.isCheckmate()) SOUNDS.check.play();
                  else if (move.flags.includes('c') || move.flags.includes('e')) SOUNDS.capture.play();
                  else SOUNDS.move.play();
                } catch(e) { /* Ignora erros de áudio */ }

                // Atualiza Streamlit
                setStateValue("uci_move", move.from + move.to + (move.promotion ? move.promotion : ''));
                setStateValue("fen", chess.fen());
                if (chess.isCheckmate()) setStateValue("game_status", "checkmate");
                else if (chess.isCheck()) setStateValue("game_status", "check");
                else if (chess.isDraw()) setStateValue("game_status", "draw");

                // Atualiza Visual
                apiRef.current?.set({
                    fen: chess.fen(),
                    turnColor: chess.turn() === 'w' ? 'white' : 'black',
                    movable: {
                        color: chess.turn() === 'w' ? 'white' : 'black',
                        dests: toDests(chess)
                    },
                    check: chess.isCheck()
                });
            }
          },
        },
      },
      animation: { enabled: true, duration: 200 },
      highlight: { lastMove: true, check: true },
    };

    apiRef.current = Chessground(boardRef.current, config);

    if (containerRef.current) {
        const resizeObserver = new ResizeObserver(() => {
            Streamlit.setFrameHeight();
            apiRef.current?.redrawAll();
        });
        resizeObserver.observe(containerRef.current);
    }

    return () => {
      apiRef.current?.destroy();
      apiRef.current = null;
    };
  }, []); 

  // Sincronização de FEN externo
  useEffect(() => {
    if (apiRef.current && fen !== chessRef.current.fen()) {
        const chess = chessRef.current;
        try { chess.load(fen); } catch (e) {}
        apiRef.current.set({
            fen: fen,
            turnColor: chess.turn() === 'w' ? 'white' : 'black',
            movable: { color: chess.turn() === 'w' ? 'white' : 'black', dests: toDests(chess) },
            check: chess.isCheck()
        });
    }
  }, [fen]);

  return (
    <div style={{ display: 'flex', justifyContent: 'center', paddingBottom: '10px' }}>
      <div 
        ref={containerRef}
        style={{ 
          position: 'relative',
          width: '500px', maxWidth: '100%', aspectRatio: '1 / 1', 
          border: '1px solid #dcdcdc', borderRadius: '4px',
          boxShadow: '0 4px 6px rgba(0,0,0,0.1)'
        }}
      >
        <div ref={boardRef} style={{ width: "100%", height: "100%" }} />
      </div>
    </div>
  );
};

export default MyComponent;