import { FC, ReactElement, useEffect, useLayoutEffect, useRef, useState, useCallback } from "react";
import { Chessground } from "chessground";
import type { Api } from "chessground/api";
import type { Config } from "chessground/config";
import { Streamlit } from "streamlit-component-lib";
import { Chess, Move } from "chess.js";

import "chessground/assets/chessground.base.css";
import "chessground/assets/chessground.cburnett.css"; 

// Interface para o objeto de lances que virá do Python
export interface TopMove {
  san: string;
  games: number;
  white_elo: number;
  black_elo: number;
  w_wins: number;
  draws: number;
  b_wins: number;
}

export interface TopGame {
  id: string;
  white: string;
  black: string;
  white_elo: number;
  black_elo: number;
  result: string;
  date: number | string;
  move: string;
}

interface MyComponentProps {
  fen: string;
  orientation?: "white" | "black";
  explorerData?: { moves: TopMove[], games: TopGame[] };
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

const MyComponent: FC<MyComponentProps> = ({ fen: initialFen, orientation: propOrientation = "white", explorerData = { moves: [], games: [] } }): ReactElement => {
  // FIX DO TRAVAMENTO: Guarda a verdadeira posição inicial e não muda quando o Python devolve um FEN novo
  const [rootFen] = useState(initialFen);

  // Refs
  const containerRef = useRef<HTMLDivElement>(null);
  const boardWrapperRef = useRef<HTMLDivElement>(null); 
  const boardRef = useRef<HTMLDivElement>(null); 
  const listRef = useRef<HTMLDivElement>(null);
  
  const apiRef = useRef<Api | null>(null);
  const gameRef = useRef(new Chess(rootFen)); 
  
  const [fen, setFen] = useState(rootFen);
  const [orientation, setOrientation] = useState<"white" | "black">(propOrientation);
  const [history, setHistory] = useState<Move[]>([]);
  const [currentMoveIndex, setCurrentMoveIndex] = useState(-1);
  const [pgn, setPgn] = useState("");
  
  // NOVO: Controle de exibição da janela do explorador
  const [showExplorer, setShowExplorer] = useState(false);

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
  // Adicionamos um parâmetro para saber se estamos apenas "espiando" um lance anterior
  const updatePython = (chessInstance: Chess, isNavigation: boolean = false) => {
      const lastMove = chessInstance.history({verbose: true}).pop();
      const uciMove = lastMove ? lastMove.from + lastMove.to + (lastMove.promotion || '') : '';
      let status = "ongoing";
      if (chessInstance.isCheckmate()) status = "checkmate";
      else if (chessInstance.isCheck()) status = "check";
      else if (chessInstance.isDraw()) status = "draw";
      
      Streamlit.setComponentValue({
          fen: chessInstance.fen(), // É este FEN que faz o Turso buscar as jogadas certas!
          pgn: isNavigation ? pgn : chessInstance.pgn(), // Se estiver só navegando, mantém o PGN cheio
          history: isNavigation ? history : chessInstance.history(),
          last_move: lastMove,
          uci_move: uciMove,
          game_status: status
      });
  };

  // --- NAVEGAÇÃO ---
  const jumpToMove = useCallback((index: number) => {
      const targetIndex = Math.max(-1, Math.min(index, history.length - 1));
      // Usa a raiz verdadeira que nunca muda
      const tempChess = new Chess(rootFen); 
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
      
      // AVISAR O PYTHON DA NOVA POSIÇÃO PARA ATUALIZAR O EXPLORADOR!
      updatePython(tempChess, true);
  }, [history, rootFen, pgn]);

// --- DELETAR LANCES ---
  const deleteCurrentMove = () => {
      if (currentMoveIndex < 0) return;

      // Apaga de forma silenciosa e instantânea sem janelas pop-up
      const newHistory = history.slice(0, currentMoveIndex);
      const newGame = new Chess(rootFen); // Usa a raiz verdadeira
      newHistory.forEach(m => newGame.move(m));
      
      gameRef.current = newGame;
      setHistory(newHistory);
      setCurrentMoveIndex(newHistory.length - 1);
      setFen(newGame.fen());
      setPgn(newGame.pgn());
      
      updatePython(newGame, false);

      apiRef.current?.set({
          fen: newGame.fen(),
          lastMove: newHistory.length > 0 
              ? [newHistory[newHistory.length - 1].from, newHistory[newHistory.length - 1].to] 
              : undefined,
          turnColor: newGame.turn() === 'w' ? 'white' : 'black',
          movable: {
              color: newGame.turn() === 'w' ? 'white' : 'black',
              dests: toDests(newGame)
          },
          check: newGame.isCheck()
      });
  };

  // --- LÓGICA DE EXECUTAR UM LANCE ---
  const executeMove = (movePayload: string | { from: string, to: string, promotion?: string }) => {
      // Bloqueio rigoroso: se estiver espionando o passado, não deixa jogar (protege a linha original)
      if (currentMoveIndex < history.length - 1) {
          apiRef.current?.set({ fen: gameRef.current.fen() }); 
          return;
      }
      
      try {
          const move = gameRef.current.move(movePayload);
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
              
              updatePython(gameRef.current, false);

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
      } catch (e) { 
          apiRef.current?.set({ fen: gameRef.current.fen() }); 
      }
  };

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
           executeMove({ from: orig, to: dest, promotion: 'q' });
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
             Streamlit.setFrameHeight(containerRef.current.scrollHeight);
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

{/* Foi adicionado position: 'relative' no container pai abaixo para alinhar o overlay */}
            <div style={{ flex: '1 1 150px', display: 'flex', flexDirection: 'column', border: '1px solid #ddd', borderRadius: '4px', backgroundColor: '#fff', height: '450px', position: 'relative' }}>
                <div style={{ padding: '8px', backgroundColor: '#f6f6f6', borderBottom: '1px solid #ddd', fontWeight: 'bold', fontSize: '13px', textAlign: 'center' }}>Histórico</div>
                
                <div ref={listRef} style={{ flex: 1, overflowY: 'auto', padding: '5px', height: '0px' }}>
                    {history.length === 0 ? <div style={{color:'#aaa', textAlign:'center', marginTop:'20px'}}>...</div> : renderMoveList()}
                </div>

                {/* OVERLAY DO EXPLORADOR DA BASE DE DADOS */}
                {showExplorer && (
                    <div style={{ position: 'absolute', top: '35px', left: 0, width: '100%', height: 'calc(100% - 35px)', backgroundColor: 'rgba(255, 255, 255, 0.96)', zIndex: 10, overflowY: 'auto', borderTop: '1px solid #ddd', backdropFilter: 'blur(2px)', display: 'flex', flexDirection: 'column' }}>
                        {explorerData.moves.length === 0 ? (
                            <div style={{ padding: '20px', textAlign: 'center', color: '#666', fontSize: '12px' }}>Nenhuma partida encontrada nesta posição.</div>
                        ) : (
                            <>
                                {/* 1. SEÇÃO DOS LANCES (TABELA COM GRÁFICO) */}
                                <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '12px', textAlign: 'left', tableLayout: 'fixed' }}>
                                    <tbody>
                                        {explorerData.moves.map((m, idx) => {
                                            const wPct = Math.round((m.w_wins / m.games) * 100) || 0;
                                            const dPct = Math.round((m.draws / m.games) * 100) || 0;
                                            const bPct = Math.round((m.b_wins / m.games) * 100) || 0;
                                            
                                            return (
                                                <tr key={idx} 
                                                    onClick={() => executeMove(m.san)}
                                                    style={{ borderBottom: '1px solid #eee', cursor: 'pointer', transition: 'background-color 0.2s' }}
                                                    onMouseOver={(e) => e.currentTarget.style.backgroundColor = '#dbeafe'}
                                                    onMouseOut={(e) => e.currentTarget.style.backgroundColor = 'transparent'}
                                                >
                                                    <td style={{ padding: '6px', fontWeight: 'bold', width: '20%' }}>{m.san}</td>
                                                    <td style={{ padding: '6px', width: '20%', color: '#666' }}>{m.games}</td>
                                                    
                                                    {/* CÉLULA DO GRÁFICO DE BARRAS */}
                                                    <td style={{ padding: '6px', width: '60%' }}>
                                                        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '9px', color: '#888', marginBottom: '2px', padding: '0 2px' }}>
                                                            <span>{wPct > 0 ? `${wPct}%` : ''}</span>
                                                            <span>{dPct > 0 ? `${dPct}%` : ''}</span>
                                                            <span>{bPct > 0 ? `${bPct}%` : ''}</span>
                                                        </div>
                                                        <div style={{ display: 'flex', width: '100%', height: '4px', borderRadius: '2px', overflow: 'hidden', border: '1px solid #ddd' }}>
                                                            {wPct > 0 && <div style={{ width: `${wPct}%`, backgroundColor: '#eee' }} title={`Brancas: ${wPct}%`} />}
                                                            {dPct > 0 && <div style={{ width: `${dPct}%`, backgroundColor: '#a0a0a0' }} title={`Empates: ${dPct}%`} />}
                                                            {bPct > 0 && <div style={{ width: `${bPct}%`, backgroundColor: '#444' }} title={`Pretas: ${bPct}%`} />}
                                                        </div>
                                                    </td>
                                                </tr>
                                            );
                                        })}
                                    </tbody>
                                </table>

                                {/* 2. SEÇÃO DAS MELHORES PARTIDAS */}
                                <div style={{ marginTop: 'auto', borderTop: '2px solid #ccc', backgroundColor: '#fafafa' }}>
                                    <div style={{ padding: '6px 8px', fontSize: '11px', fontWeight: 'bold', color: '#555', borderBottom: '1px solid #eee' }}>Top Partidas</div>
                                    <div style={{ maxHeight: '200px', overflowY: 'auto' }}>
                                        {explorerData.games.map((g, idx) => {
                                            // Converte o Timestamp milissegundos para Data Local Brasileira
                                            const gameDate = g.date ? new Date(Number(g.date)).toLocaleDateString('pt-BR') : '';
                                            return (
                                                <a key={idx} href={`https://lichess.org/${g.id}`} target="_blank" rel="noreferrer" 
                                                   style={{ display: 'block', padding: '6px 8px', textDecoration: 'none', color: 'inherit', borderBottom: '1px solid #eee', transition: 'background-color 0.2s' }}
                                                   onMouseOver={(e) => e.currentTarget.style.backgroundColor = '#eaeaea'}
                                                   onMouseOut={(e) => e.currentTarget.style.backgroundColor = 'transparent'}
                                                >
                                                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '11px' }}>
                                                        
                                                        {/* NOVO BLOCO: O LANCE JOGADO */}
                                                        <div style={{ fontWeight: 'bold', fontSize: '13px', width: '45px', textAlign: 'center', color: '#1f2937', backgroundColor: '#e5e7eb', padding: '4px 0', borderRadius: '4px', marginRight: '10px' }}>
                                                            {g.move}
                                                        </div>
                                                        
                                                        <div style={{ flex: 1, overflow: 'hidden' }}>
                                                            <div style={{ display: 'flex', gap: '6px', alignItems: 'center', marginBottom: '3px' }}>
                                                                <span style={{ display: 'inline-block', minWidth: '10px', height: '10px', backgroundColor: '#fff', border: '1px solid #ccc' }}></span>
                                                                <span style={{ color: '#666', fontWeight: 'bold', width: '30px' }}>{g.white_elo}</span>
                                                                <span style={{ whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>{g.white}</span>
                                                            </div>
                                                            <div style={{ display: 'flex', gap: '6px', alignItems: 'center' }}>
                                                                <span style={{ display: 'inline-block', minWidth: '10px', height: '10px', backgroundColor: '#000', border: '1px solid #000' }}></span>
                                                                <span style={{ color: '#666', fontWeight: 'bold', width: '30px' }}>{g.black_elo}</span>
                                                                <span style={{ whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>{g.black}</span>
                                                            </div>
                                                        </div>
                                                        <div style={{ textAlign: 'right', minWidth: '45px' }}>
                                                            <div style={{ fontWeight: 'bold', backgroundColor: '#ddd', padding: '2px 4px', borderRadius: '3px', display: 'inline-block' }}>{g.result}</div>
                                                            <div style={{ color: '#888', marginTop: '3px', fontSize: '10px' }}>{gameDate}</div>
                                                        </div>
                                                    </div>
                                                </a>
                                            );
                                        })}
                                    </div>
                                </div>
                            </>
                        )}
                    </div>
                )}
            </div>
        </div>

        <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
            <button style={btnStyle} onClick={() => setOrientation(o => o === "white" ? "black" : "white")}>🔄 Girar</button>
            <button style={btnStyle} onClick={() => jumpToMove(-1)}>⏪</button>
            <button style={btnStyle} onClick={() => jumpToMove(currentMoveIndex - 1)}>◀</button>
            <button style={btnStyle} onClick={() => jumpToMove(currentMoveIndex + 1)}>▶</button>
            <button style={btnStyle} onClick={() => jumpToMove(history.length - 1)}>⏩</button>
            
            {/* NOVO BOTÃO APAGAR */}
            <button 
                style={{...btnStyle, color: '#dc2626', opacity: currentMoveIndex >= 0 ? 1 : 0.5}} 
                onClick={deleteCurrentMove}
                disabled={currentMoveIndex < 0}
                title="Apagar este lance e a continuação"
            >
                🗑️ Apagar
            </button>

            <button 
                style={{...btnStyle, backgroundColor: showExplorer ? '#dbeafe' : '#f9f9f9', fontWeight: showExplorer ? 'bold' : 'normal'}} 
                onClick={() => setShowExplorer(!showExplorer)}
            >
                {showExplorer ? "❌ Fechar Explorador" : "🔎 Explorador"}
            </button>
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