import { FrontendRendererArgs } from "@streamlit/component-v2-lib";
import { FC, ReactElement, useEffect, useRef } from "react";
import { Chessground } from "chessground";
import "chessground/assets/chessground.base.css";
// Tema (escolha um dos dois, o brown é o padrão madeira)
import "chessground/assets/chessground.brown.css";


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

const MyComponent: FC<MyComponentProps> = ({
  fen,
  setStateValue,
}): ReactElement => {
  /**
   * Referência para o container do tabuleiro.
   * Chessground manipula o DOM diretamente.
   */
  const boardRef = useRef<HTMLDivElement | null>(null);

  /**
   * Inicializa o Chessground uma única vez.
   */
  useEffect(() => {
    if (!boardRef.current) return;

    const cg = Chessground(boardRef.current, {
      orientation: "white",
      coordinates: true,

      movable: {
        free: false,
        color: "both",
      },

      highlight: {
        lastMove: true,
        check: true,
      },

      /**
       * Callback de movimento (origem → destino)
       * Aqui nasce o lance UCI.
       */
      events: {
        move: (from, to) => {
          const uci = `${from}${to}`;
          setStateValue("uci_move", uci);
        },
      },
    });

    return () => {
      cg.destroy?.();
    };
  }, [setStateValue]);

  /**
   * Atualiza a posição quando o FEN muda.
   */
  useEffect(() => {
    if (!boardRef.current) return;

    // Chessground expõe o estado via DOM
    Chessground(boardRef.current).set({
      fen: fen,
    });
  }, [fen]);

  return (
    <div
      ref={boardRef}
      style={{
        width: "480px",
        height: "480px",
        margin: "0 auto",
      }}
    />
  );
};

export default MyComponent;
