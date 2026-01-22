import { FC, ReactElement, useEffect, useRef } from "react";
import { Chessground } from "chessground";
import type { Api } from "chessground/api";
import type { Config } from "chessground/config";

// CSS do tabuleiro
import "chessground/assets/chessground.base.css";
import "chessground/assets/chessground.brown.css";

// Definindo os tipos manualmente para não depender de bibliotecas externas complexas
interface MyComponentProps {
  fen: string;
  setStateValue: (key: string, value: any) => void;
}

const MyComponent: FC<MyComponentProps> = ({ fen, setStateValue }): ReactElement => {
  const boardRef = useRef<HTMLDivElement | null>(null);
  const apiRef = useRef<Api | null>(null);

  // Inicialização (Montagem)
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
            // Manda o movimento para o index.tsx, que manda para o Python
            setStateValue("uci_move", uci);
          },
        },
      },
      animation: { enabled: true, duration: 200 },
    };

    apiRef.current = Chessground(boardRef.current, config);

    return () => {
      apiRef.current?.destroy();
      apiRef.current = null;
    };
  }, []); // Array vazio = roda só uma vez

  // Atualização (Quando o FEN muda)
  useEffect(() => {
    if (apiRef.current) {
      apiRef.current.set({ fen: fen });
    }
  }, [fen]);

  return (
    <div style={{ 
      display: 'flex', 
      justifyContent: 'center',
      padding: '10px'
    }}>
      {/* Container do Tabuleiro */}
      <div
        ref={boardRef}
        style={{
          width: "500px",  
          height: "500px", 
          border: "5px solid #4a4a4a"
        }}
      />
    </div>
  );
};

export default MyComponent;