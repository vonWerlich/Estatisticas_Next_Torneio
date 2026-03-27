import os

# Extensões que você quer que a IA leia
EXTENSOES = ('.py', '.md', '.json', '.sql') 
# Pastas ou arquivos para ignorar
IGNORAR = ('venv', '__pycache__', '.git', 'data', 'player_data') 

with open("MEU_PROJETO_PARA_IA.txt", "w", encoding="utf-8") as outfile:
    for root, dirs, files in os.walk("."):
        # Pula as pastas ignoradas
        dirs[:] = [d for d in dirs if d not in IGNORAR] 
        
        for file in files:
            if file.endswith(EXTENSOES):
                caminho_completo = os.path.join(root, file)
                outfile.write(f"\n{'='*60}\n")
                outfile.write(f"ARQUIVO: {caminho_completo}\n")
                outfile.write(f"{'='*60}\n\n")
                
                try:
                    with open(caminho_completo, "r", encoding="utf-8") as infile:
                        outfile.write(infile.read())
                except Exception as e:
                    outfile.write(f"[Erro ao ler arquivo: {e}]\n")

print("✅ Arquivo MEU_PROJETO_PARA_IA.txt gerado com sucesso!")