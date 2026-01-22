import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  // Garante caminhos relativos (essencial para o Streamlit)
  base: "./",
  
  plugins: [react()],
  
  build: {
    outDir: "build",
    emptyOutDir: true,
    // REMOVEMOS A PARTE 'lib' AQUI.
    // Isso força o Vite a olhar para o seu index.html e construir o site a partir dele.
  },
  
  server: {
    port: 3000,
  },
});