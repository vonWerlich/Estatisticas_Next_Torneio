import { FrontendRendererArgs } from "@streamlit/component-v2-lib";
import {
  CSSProperties,
  FC,
  ReactElement,
  useCallback,
  useMemo,
  useState,
} from "react";

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
  // Por enquanto, só exibimos o FEN para validar o contrato
  // O tabuleiro entra na próxima etapa

  return (
    <div style={{ padding: "8px", fontFamily: "monospace" }}>
      <div>FEN recebida do Python:</div>
      <div>{fen}</div>

      <button
        onClick={() => {
          // Simulação temporária de um lance
          setStateValue("uci_move", "e2e4");
        }}
      >
        Simular lance e2e4
      </button>
    </div>
  );
};

export default MyComponent;
