import requests
import json
import os
import sys

# --- 1. CORREÇÃO DE CODIFICAÇÃO PARA O TERMINAL WINDOWS ---
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

# --- CONFIGURAÇÃO ---
TEAM_ID = "next-nucleo-de-estudos-em-xadrez--tecnologias"
DATA_DIR_PLAYERS = "player_data"
PLAYER_DB_FILE = os.path.join(DATA_DIR_PLAYERS, "players.json")
OUTPUT_FILE = os.path.join(DATA_DIR_PLAYERS, "lurkers.json") 

def carregar_json(filepath):
    if not os.path.exists(filepath): return []
    try:
        with open(filepath, "r", encoding="utf-8") as f: return json.load(f)
    except: return []

def salvar_json(filepath, data):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def main():
    print(f"--- GERADOR DE LISTA DE MEMBROS SEM JOGOS (V2) ---")
    
    # 1. Carregar DB Local e Normalizar IDs (Lowercase)
    players_db = carregar_json(PLAYER_DB_FILE)
    
    # Criamos um SET com os IDs minúsculos de quem já jogou.
    # Isso evita problemas de Case Sensitivity (Ex: "Player1" vs "player1")
    local_ids_set = set()
    for p in players_db:
        if p.get('username'):
            local_ids_set.add(p['username'].lower())
            
    print(f"📂 Jogadores no banco local (que participaram): {len(local_ids_set)}")
    
    # 2. Baixar lista oficial da equipe
    print(f"📡 Baixando membros da equipe '{TEAM_ID}'...")
    url = f"https://lichess.org/api/team/{TEAM_ID}/users"
    
    lurkers_list = []
    total_team_members = 0
    
    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            for line in r.iter_lines():
                if line:
                    total_team_members += 1
                    data = json.loads(line.decode('utf-8'))
                    
                    # Pega o ID (sempre minúsculo e confiável)
                    lichess_id = data.get("id")
                    
                    # Tenta pegar o Username bonitinho, se falhar usa o ID
                    display_name = data.get("username")
                    if not display_name:
                        display_name = lichess_id  # Fallback
                    
                    # --- O DIFF ACONTECE AQUI ---
                    # Compara ID com ID. Infalível.
                    if lichess_id not in local_ids_set:
                        lurkers_list.append({
                            "username": display_name,
                            "id_lichess": lichess_id,
                            "last_seen_api": data.get("seenAt"),
                            "joined_team": True
                        })
                        
    except Exception as e:
        print(f"❌ Erro ao baixar membros: {e}")
        return

    # 3. Relatório e Salvamento
    print(f"\n📊 Estatísticas Reais:")
    print(f"   - Total de membros na equipe (API): {total_team_members}")
    print(f"   - Total que já jogaram (DB Local): {len(local_ids_set)}")
    
    # A conta deve bater: Total Equipe - Quem Jogou = Lurkers
    print(f"   - Membros que NUNCA jogaram (Lurkers): {len(lurkers_list)}")
    
    if lurkers_list:
        salvar_json(OUTPUT_FILE, lurkers_list)
        print(f"\n✅ Lista corrigida salva em: {OUTPUT_FILE}")
        
        # Mostra alguns exemplos para verificar se o 'username' parou de vir null
        print("   Exemplos de Lurkers encontrados:")
        for l in lurkers_list[:5]:
            print(f"   - {l['username']} (Visto em: {l['last_seen_api']})")
    else:
        print("\n✅ Todos os membros da equipe já participaram de algum torneio.")

if __name__ == "__main__":
    main()