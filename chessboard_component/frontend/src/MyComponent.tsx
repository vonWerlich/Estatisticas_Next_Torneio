import { FrontendRendererArgs } from "@streamlit/component-v2-lib";
import { FC, ReactElement, useEffect, useRef } from "react";

import { Chessground } from "chessground";
import type { Api } from "chessground/api";
import type { Config } from "chessground/config";

import "chessground/assets/chessground.base.css";
import "chessground/assets/chessground.brown.css"; //tema clássico


// --------- Tipos do contrato com o Streamlit ---------

export type MyComponentStateShape = {
  uci_move: string | null;
};

export type MyComponentDataShape = {
  fen: string;
};

export type MyComponentProps = Pick<
  FrontendRendererArgs<MyComponentStateShape, MyComponentDataShape>,
  "setStateValue"
> &
  MyComponentDataShape;


// --------- Componente ---------

const MyComponent: FC<MyComponentProps> = ({
  fen,
  setStateValue,
}): ReactElement => {
  const boardRef = useRef<HTMLDivElement | null>(null);
  const apiRef = useRef<Api | null>(null);

  // Inicializa o Chessground UMA vez
  useEffect(() => {
    if (!boardRef.current) return;

    const config: Config = {
      fen,
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
    };

    apiRef.current = Chessground(boardRef.current, config);

    return () => {
      apiRef.current?.destroy();
      apiRef.current = null;
    };
  }, []);

  // Atualiza o FEN quando o Python mudar
  useEffect(() => {
    if (apiRef.current) {
      apiRef.current.set({ fen });
    }
  }, [fen]);

return (
    <div style={{ 
      display: 'flex', 
      justifyContent: 'center', 
      padding: '20px',
      background: '#f0f0f0' // Fundo cinza para provar que o container existe
    }}>
      <div
        ref={boardRef}
        style={{
          width: "500px",       // Tamanho FIXO para garantir que não colapse
          height: "500px",      // Altura FIXA é obrigatória pro Chessground
          border: "5px solid red" // Borda de debug (remova depois)
        }}
      />
    </div>
  );
};

export default MyComponent;
