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

// --- CONFIGURAÇÃO DE SONS (PADRÃO LICHESS) ---
// Certifique-se que os arquivos estão em: chessboard_component/frontend/public/sounds/
const AUDIO_URLS = {
    move: "./sounds/public_sound_standard_Move.mp3",
    capture: "./sounds/public_sound_standard_Capture.mp3",
    notify: "./sounds/public_sound_standard_GenericNotify.mp3" // Usado para Fim de Jogo (Mate/Empate)
};

const SOUNDS = {
  move: new Audio(AUDIO_URLS.move),
  capture: new Audio(AUDIO_URLS.capture),
  notify: new Audio(AUDIO_URLS.notify),
};

// Pré-carregamento
try { Object.values(SOUNDS).forEach(s => s.load()); } catch(e) {}

const playSound = (audio: HTMLAudioElement) => {
    try {
        if (audio.readyState >= 2 || audio.HAVE_CURRENT_DATA) {
            audio.currentTime = 0;
            audio.play().catch(() => {});
        } else {
            audio.load();
            audio.play().catch(() => {});
        }
    } catch (e) {
        console.error("Audio error:", e);
    }
};

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

  // --- CSS DO TABULEIRO (MANTIDO) ---
  useLayoutEffect(() => {
    const css = `
      cg-board {
        background-image: conic-gradient(
          #b58863 90deg, #f0d9b5 90deg 180deg, 
          #b58863 180deg 270deg, #f0d9b5 270deg
        ) !important;
        background-size: 25% 25% !important;
        background-color: #f0d9b5 !important;
      }
      cg-board square.move-dest { 
        background: radial-gradient(rgba(20, 85, 30, 0.5) 19%, rgba(0, 0, 0, 0) 20%) !important; 
      }
      cg-board square.oc.move-dest { 
        background-image: 
            linear-gradient(to bottom right, rgba(20, 85, 30, 0.6) 15%, transparent 15%),
            linear-gradient(to bottom left, rgba(20, 85, 30, 0.6) 15%, transparent 15%),
            linear-gradient(to top right, rgba(20, 85, 30, 0.6) 15%, transparent 15%),
            linear-gradient(to top left, rgba(20, 85, 30, 0.6) 15%, transparent 15%) !important;
      }
      cg-board square.move-dest:hover { background: rgba(20, 85, 30, 0.3) !important; }
      cg-board square.last-move { background-color: rgba(155, 199, 0, 0.41) !important; }
      cg-board square.selected { background-color: rgba(20, 85, 30, 0.5) !important; }
      cg-board square.check { background: radial-gradient(ellipse at center, rgba(255, 0, 0, 1) 0%, rgba(231, 0, 0, 1) 25%, rgba(169, 0, 0, 0) 89%, rgba(158, 0, 0, 0) 100%) !important; }
      
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

  // --- LÓGICA DO JOGO ---
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
            const moveAttempt = { from: orig, to: dest, promotion: 'q' };
            const move = chess.move(moveAttempt); 
            
            if (move) {
                // --- LÓGICA DE SOM PADRÃO LICHESS ---
                const isGameOver = chess.isGameOver(); // Mate, Empate, Afogamento...
                const isCapture = move.flags.includes('c') || move.flags.includes('e');

                if (isGameOver) {
                    // Toca o som de notificação se o jogo acabou
                    playSound(SOUNDS.notify);
                } else if (isCapture) {
                    playSound(SOUNDS.capture);
                } else {
                    playSound(SOUNDS.move);
                }

                // Atualiza Streamlit
                setStateValue("uci_move", move.from + move.to + (move.promotion ? move.promotion : ''));
                setStateValue("fen", chess.fen());
                
                let status = "ongoing";
                if (chess.isCheckmate()) status = "checkmate";
                else if (chess.isCheck()) status = "check";
                else if (chess.isDraw()) status = "draw";
                setStateValue("game_status", status);

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