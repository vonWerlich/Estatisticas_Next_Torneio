import os

# 1. Pega a pasta onde este script está
DIR_ATUAL = os.path.dirname(os.path.abspath(__file__))
# 2. Sobe para a raiz do projeto (ajuste se o script estiver em outra pasta)
RAIZ_DO_PROJETO = os.path.dirname(DIR_ATUAL) 

# Extensões úteis para a IA entender a lógica e estrutura
EXTENSOES = ('.py', '.md', '.json', '.sql', '.yaml', '.txt', '.js', '.jsx', '.ts', '.tsx', '.html') 
# Pastas que não contêm código/lógica (ignorar 'data' evita ler o banco .db por erro)
IGNORAR_DIRS = ('venv', '__pycache__', '.git', 'data', 'player_data', '.streamlit', 'node_modules', 'build', 'dist')

with open("MEU_PROJETO_PARA_IA.txt", "w", encoding="utf-8") as outfile:
    # Usamos RAIZ_DO_PROJETO em vez de "." para garantir o escopo total
    for root, dirs, files in os.walk(RAIZ_DO_PROJETO):
        # Filtra pastas ignoradas
        dirs[:] = [d for d in dirs if d not in IGNORAR_DIRS] 
        
        for file in files:
            if file.endswith(EXTENSOES):
                # Não queremos que o script leia o próprio arquivo de saída
                if file == "MEU_PROJETO_PARA_IA.txt":
                    continue
                    
                caminho_completo = os.path.join(root, file)
                # Caminho relativo para facilitar a leitura da IA
                caminho_relativo = os.path.relpath(caminho_completo, RAIZ_DO_PROJETO)
                
                outfile.write(f"\n{'='*60}\n")
                outfile.write(f"ARQUIVO: {caminho_relativo}\n")
                outfile.write(f"{'='*60}\n\n")
                
                try:
                    with open(caminho_completo, "r", encoding="utf-8") as infile:
                        outfile.write(infile.read())
                        outfile.write("\n")
                except Exception as e:
                    outfile.write(f"[Erro ao ler arquivo: {e}]\n")

print(f"✅ Projeto mapeado a partir de: {RAIZ_DO_PROJETO}")
print("✅ Arquivo MEU_PROJETO_PARA_IA.txt gerado com sucesso!")