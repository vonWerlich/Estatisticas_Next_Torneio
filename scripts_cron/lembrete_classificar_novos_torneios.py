name: Lembrete Classificador NEXT

on:
  schedule:
    # Atenção ao fuso horário (explicado abaixo)
    - cron: '0 12 31 7,12 *'

jobs:
  mandar-lembrete:
    runs-on: ubuntu-latest
    steps:
      # Baixa o seu código para o servidor do GitHub
      - name: Checkout do código
        uses: actions/checkout@v4

      # Instala o Python
      - name: Configurar Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      # Instala a biblioteca 'requests' necessária para o Ntfy
      - name: Instalar requests
        run: pip install requests

      # Roda o seu script
      - name: Disparar notificação
        run: python scripts_cron/lembrete_classificador.py