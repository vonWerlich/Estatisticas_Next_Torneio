import { FC, ReactElement, useEffect, useLayoutEffect, useRef, useState, useCallback } from "react";
import { Chessground } from "chessground";
import type { Api } from "chessground/api";
import type { Config } from "chessground/config";
import { Streamlit } from "streamlit-component-lib";
import { Chess, Move } from "chess.js";

import "chessground/assets/chessground.base.css";
import "chessground/assets/chessground.cburnett.css"; 

interface MyComponentProps {
  fen: string;
  orientation?: "white" | "black";
}

// --- SONS ---
const AUDIO_URLS = {
    move: "./sounds/public_sound_standard_Move.mp3",
    capture: "./sounds/public_sound_standard_Capture.mp3",
    notify: "./sounds/public_sound_standard_GenericNotify.mp3" 
};

const SOUNDS = {
  move: new Audio(AUDIO_URLS.move),
  capture: new Audio(AUDIO_URLS.capture),
  notify: new Audio(AUDIO_URLS.notify),
};
try { Object.values(SOUNDS).forEach(s => s.load()); } catch(e) {}

const playSound = (audio: HTMLAudioElement) => {
    try {
        audio.currentTime = 0;
        audio.play().catch(() => {});
    } catch (e) {}
};

const toDests = (chess: Chess) => {
  const dests = new Map();
  chess.moves({ verbose: true }).forEach((m) => {
    if (!dests.has(m.from)) dests.set(m.from, []);
    dests.get(m.from).push(m.to);
  });
  return dests;
};

const MyComponent: FC<MyComponentProps> = ({ fen: initialFen, orientation: propOrientation = "white" }): ReactElement => {
  // Refs
  const containerRef = useRef<HTMLDivElement>(null);
  const boardWrapperRef = useRef<HTMLDivElement>(null); 
  const boardRef = useRef<HTMLDivElement>(null); 
  const listRef = useRef<HTMLDivElement>(null);
  
  const apiRef = useRef<Api | null>(null);
  const gameRef = useRef(new Chess(initialFen)); 
  
  const [fen, setFen] = useState(initialFen);
  const [orientation, setOrientation] = useState<"white" | "black">(propOrientation);
  const [history, setHistory] = useState<Move[]>([]);
  const [currentMoveIndex, setCurrentMoveIndex] = useState(-1);
  const [pgn, setPgn] = useState("");

  // --- CSS INJETADO ---
  useLayoutEffect(() => {
    const css = `
      cg-board {
        background-image: conic-gradient(#b58863 90deg, #f0d9b5 90deg 180deg, #b58863 180deg 270deg, #f0d9b5 270deg) !important;
        background-size: 25% 25% !important;
      }
      cg-board square.move-dest { background: radial-gradient(rgba(20, 85, 30, 0.5) 19%, rgba(0, 0, 0, 0) 20%) !important; }
      cg-board square.oc.move-dest { 
        background-image: linear-gradient(to bottom right, rgba(20, 85, 30, 0.6) 15%, transparent 15%),
            linear-gradient(to bottom left, rgba(20, 85, 30, 0.6) 15%, transparent 15%),
            linear-gradient(to top right, rgba(20, 85, 30, 0.6) 15%, transparent 15%),
            linear-gradient(to top left, rgba(20, 85, 30, 0.6) 15%, transparent 15%) !important;
      }
      cg-board square.last-move { background-color: rgba(155, 199, 0, 0.41) !important; }
      cg-board square.selected { background-color: rgba(20, 85, 30, 0.5) !important; }
      cg-board square.check { background: radial-gradient(ellipse at center, red 0%, transparent 100%) !important; }
      .orientation-white .ranks :nth-child(odd), .orientation-white .files :nth-child(even),
      .orientation-black .ranks :nth-child(even), .orientation-black .files :nth-child(odd) { color: #f0d9b5 !important; }
      .orientation-white .ranks :nth-child(even), .orientation-white .files :nth-child(odd),
      .orientation-black .ranks :nth-child(even), .orientation-black .files :nth-child(even) { color: #b58863 !important; }
    `;
    const style = document.createElement('style');
    style.innerHTML = css;
    document.head.appendChild(style);
    return () => { if(document.head.contains(style)) document.head.removeChild(style); };
  }, []);

  // --- PYTHON UPDATE ---
  const updatePython = (chess: Chess) => {
      const lastMove = chess.history({verbose: true}).pop();
      const uciMove = lastMove ? lastMove.from + lastMove.to + (lastMove.promotion || '') : '';
      let status = "ongoing";
      if (chess.isCheckmate()) status = "checkmate";
      else if (chess.isCheck()) status = "check";
      else if (chess.isDraw()) status = "draw";
      
      Streamlit.setComponentValue({
          fen: chess.fen(),
          pgn: chess.pgn(),
          history: chess.history(),
          last_move: lastMove,
          uci_move: uciMove,
          game_status: status
      });
  };

  // --- NAVEGAÇÃO ---
  const jumpToMove = useCallback((index: number) => {
      const targetIndex = Math.max(-1, Math.min(index, history.length - 1));
      const tempChess = new Chess(); 
      for (let i = 0; i <= targetIndex; i++) tempChess.move(history[i]);
      
      const newFen = tempChess.fen();
      setCurrentMoveIndex(targetIndex);
      setFen(newFen);
      
      const isLatest = targetIndex === history.length - 1;

      apiRef.current?.set({
          fen: newFen,
          lastMove: targetIndex >= 0 ? [history[targetIndex].from, history[targetIndex].to] : undefined,
          check: tempChess.isCheck(),
          turnColor: tempChess.turn() === 'w' ? 'white' : 'black',
          movable: {
              color: isLatest ? (tempChess.turn() === 'w' ? 'white' : 'black') : undefined,
              dests: isLatest ? toDests(tempChess) : new Map()
          }
      });
  }, [history]);

  // --- INICIALIZAÇÃO E RESIZE ---
  useEffect(() => {
    if (!boardRef.current) return;

    // Configuração Chessground
    const config: Config = {
      fen: fen,
      orientation: orientation,
      movable: {
        color: 'white',
        free: false,
        dests: toDests(gameRef.current),
        showDests: true,
      },
      animation: { enabled: true, duration: 200 },
      highlight: { lastMove: true, check: true },
      events: {
        move: (orig, dest) => {
          if (currentMoveIndex < history.length - 1) {
              apiRef.current?.set({ fen: gameRef.current.fen() }); 
              return;
          }

          try {
              const move = gameRef.current.move({ from: orig, to: dest, promotion: 'q' });
              if (move) {
                  const isCap = move.flags.includes('c') || move.flags.includes('e');
                  if (gameRef.current.isGameOver()) playSound(SOUNDS.notify);
                  else if (isCap) playSound(SOUNDS.capture);
                  else playSound(SOUNDS.move);

                  const newHist = gameRef.current.history({ verbose: true });
                  setHistory(newHist);
                  setCurrentMoveIndex(newHist.length - 1);
                  setFen(gameRef.current.fen());
                  setPgn(gameRef.current.pgn());
                  
                  updatePython(gameRef.current);

                  apiRef.current?.set({
                      fen: gameRef.current.fen(),
                      turnColor: gameRef.current.turn() === 'w' ? 'white' : 'black',
                      movable: {
                          color: gameRef.current.turn() === 'w' ? 'white' : 'black',
                          dests: toDests(gameRef.current)
                      },
                      check: gameRef.current.isCheck()
                  });
              }
          } catch (e) { apiRef.current?.set({ fen: gameRef.current.fen() }); }
        }
      }
    };

    apiRef.current = Chessground(boardRef.current, config);
    
    // --- OBSERVER ---
    const resizeObserver = new ResizeObserver((entries) => {
        let shouldRedrawBoard = false;
        
        for (const entry of entries) {
            if (entry.target === boardWrapperRef.current) {
                shouldRedrawBoard = true;
            }
        }

        if (shouldRedrawBoard) {
            apiRef.current?.redrawAll();
        }

        // Ajusta a altura do Streamlit baseado no container TOTAL
        if (containerRef.current) {
             Streamlit.setFrameHeight(containerRef.current.scrollHeight + 10);
        }
    });

    if (boardWrapperRef.current) resizeObserver.observe(boardWrapperRef.current);
    if (containerRef.current) resizeObserver.observe(containerRef.current);

    // Foco inicial
    containerRef.current?.focus();

    return () => {
        apiRef.current?.destroy();
        resizeObserver.disconnect();
    };
  }, []); 

  // Orientação Sync
  useEffect(() => { apiRef.current?.set({ orientation }); }, [orientation]);

  // Teclado Sync
  useEffect(() => {
      const handleKeyDown = (e: KeyboardEvent) => {
          if (["INPUT", "TEXTAREA"].includes((e.target as HTMLElement).tagName)) return;

          let handled = true;
          if (e.key === "ArrowLeft") jumpToMove(currentMoveIndex - 1);
          else if (e.key === "ArrowRight") jumpToMove(currentMoveIndex + 1);
          else if (e.key === "ArrowUp") jumpToMove(-1);
          else if (e.key === "ArrowDown") jumpToMove(history.length - 1);
          else if (e.key.toLowerCase() === "f") setOrientation(o => o === "white" ? "black" : "white");
          else handled = false;

          if (handled) e.preventDefault();
      };
      window.addEventListener("keydown", handleKeyDown);
      return () => window.removeEventListener("keydown", handleKeyDown);
  }, [currentMoveIndex, history, jumpToMove]);

  // Scroll
  useEffect(() => {
    if (listRef.current) listRef.current.scrollTop = listRef.current.scrollHeight;
  }, [history.length]);

  const renderMoveList = () => {
      const rows = [];
      for (let i = 0; i < history.length; i += 2) {
          const w = history[i];
          const b = history[i + 1];
          rows.push(
              <div key={i} style={{ display: 'flex', borderBottom: '1px solid #eee', padding: '2px 4px', fontSize: '13px' }}>
                  <span style={{ width: '25px', color: '#999' }}>{Math.floor(i / 2) + 1}.</span>
                  <span onClick={() => jumpToMove(i)} style={moveItemStyle(i === currentMoveIndex)}>{w.san}</span>
                  {b && <span onClick={() => jumpToMove(i + 1)} style={moveItemStyle(i + 1 === currentMoveIndex)}>{b.san}</span>}
              </div>
          );
      }
      return rows;
  };

  return (
    <div 
      ref={containerRef} 
      tabIndex={0} 
      style={{ 
        display: 'flex', 
        flexDirection: 'column', 
        gap: '10px', 
        padding: '10px', 
        fontFamily: 'sans-serif',
        minWidth: '300px', 
        width: '100%',
        backgroundColor: '#fff',
        boxSizing: 'border-box'
      }}
    >
        <div style={{ display: 'flex', gap: '15px', alignItems: 'flex-start', flexWrap: 'wrap', flex: '1 1 auto' }}>
            
            {/* WRAPPER DO TABULEIRO (RESIZE HORIZONTAL + SQUARE RATIO) */}
            <div 
                ref={boardWrapperRef}
                style={{
                    // CORREÇÃO: resize horizontal força o usuário a mudar apenas largura.
                    // Aspect-ratio cuida da altura automaticamente.
                    resize: 'horizontal', 
                    overflow: 'hidden', 
                    aspectRatio: '1 / 1', // Garante que seja sempre quadrado
                    minWidth: '200px', 
                    width: '450px', // Tamanho inicial
                    maxWidth: '100%',
                    position: 'relative',
                    border: '1px solid #ddd',
                    borderRadius: '4px'
                }}
            >
                <div ref={boardRef} style={{ width: '100%', height: '100%' }} />
            </div>

            <div style={{ flex: '1 1 150px', display: 'flex', flexDirection: 'column', border: '1px solid #ddd', borderRadius: '4px', backgroundColor: '#fff', height: '450px' }}>
                <div style={{ padding: '8px', backgroundColor: '#f6f6f6', borderBottom: '1px solid #ddd', fontWeight: 'bold', fontSize: '13px', textAlign: 'center' }}>Histórico</div>
                <div ref={listRef} style={{ flex: 1, overflowY: 'auto', padding: '5px', height: '0px' }}>
                    {history.length === 0 ? <div style={{color:'#aaa', textAlign:'center', marginTop:'20px'}}>...</div> : renderMoveList()}
                </div>
            </div>
        </div>

        <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
            <button style={btnStyle} onClick={() => setOrientation(o => o === "white" ? "black" : "white")}>🔄 Girar</button>
            <button style={btnStyle} onClick={() => jumpToMove(-1)}>⏪</button>
            <button style={btnStyle} onClick={() => jumpToMove(currentMoveIndex - 1)}>◀</button>
            <button style={btnStyle} onClick={() => jumpToMove(currentMoveIndex + 1)}>▶</button>
            <button style={btnStyle} onClick={() => jumpToMove(history.length - 1)}>⏩</button>
        </div>

        <div style={{ display: 'grid', gap: '8px', marginTop: '5px' }}>
          {/* Campo do FEN - Agora com altura inicial maior */}
          <div style={{ fontSize: '11px', color: '#666', fontWeight: 'bold' }}>FEN:</div>
          <textarea 
              readOnly 
              value={fen} 
              rows={2} // Aumenta a altura inicial para 2 linhas
              style={{...inputStyle, height: 'auto', resize: 'vertical', minHeight: '40px'}} 
              onClick={(e) => e.currentTarget.select()} 
          />

          {/* Campo do PGN - Agora com mais espaço inicial */}
          <div style={{ fontSize: '11px', color: '#666', fontWeight: 'bold' }}>PGN:</div>
          <textarea 
              readOnly 
              value={pgn} 
              rows={4} // Começa com 4 linhas para exibir mais lances
              style={{...inputStyle, height: 'auto', resize: 'vertical', minHeight: '80px'}} 
              onClick={(e) => e.currentTarget.select()} 
          />
      </div>
    </div>
  );
};

const moveItemStyle = (active: boolean) => ({
    cursor: 'pointer', flex: 1, paddingLeft: '4px', borderRadius: '3px',
    fontWeight: active ? 'bold' : 'normal', backgroundColor: active ? '#dbeafe' : 'transparent'
});
const btnStyle = { padding: '6px 12px', cursor: 'pointer', backgroundColor: '#f9f9f9', border: '1px solid #ccc', borderRadius: '4px', fontSize: '12px', flex: 1 };
const inputStyle = { width: '100%', padding: '6px', borderRadius: '4px', border: '1px solid #ddd', fontFamily: 'monospace', fontSize: '11px', backgroundColor: '#f9f9f9', color: '#555', boxSizing: 'border-box' as const };

export default MyComponent;