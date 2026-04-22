# ♟️ Estatísticas NEXT

O dashboard *pseudo*oficial para análise de performance e histórico de torneios do **Núcleo de Estudos em Xadrez & Tecnologias (NEXT)**.

🚀 **Acesse agora:** [torneiosnext.streamlit.app](https://torneiosnext.streamlit.app/)

---

## 🎯 O Projeto

Esta plataforma foi desenvolvida para centralizar e transformar dados brutos da API do Lichess em insights estratégicos para os membros e pesquisadores do NEXT. Através de uma interface intuitiva, é possível monitorar o crescimento da equipe, analisar a evolução de ratings e revisar partidas históricas.

## 📊 O que você encontra no Dashboard

- **Métricas de Equipe:** Visão consolidada de participação e atividade ao longo dos anos.
- **Histórico de Circuitos:** Filtros inteligentes para separar torneios Arena de sistemas Suíços.
- **Análise Individual:** Painéis dedicados a cada jogador com métricas de desempenho.
- **Ferramentas de Estudo:** Tabuleiro interativo integrado para análise rápida de posições via FEN.
- **Processamento de Dados:** Motor de busca otimizado e classificação automática de torneios.

## 🛠️ Tecnologias e Conceitos

O projeto utiliza uma arquitetura moderna de Data Science para garantir rapidez e precisão:

* **Interface:** [Streamlit](https://streamlit.io/)
* **Engine de Dados:** Pandas e DuckDB para consultas analíticas de alta performance.
* **Persistência:** SQLite para o histórico consolidado.
* **Visualização:** Gráficos interativos e componentes React customizados para o tabuleiro.

---

## 🏗️ Estrutura do Repositório

- `/views`: Lógica das páginas e interface do usuário.
- `/scripts_cron`: Rotinas de manutenção e classificação automática.
- `/components`: Elementos visuais e componentes React (TypeScript).
- `/utils`: Core do sistema, filtros e conexão com banco de dados.

---

## 🤝 Desenvolvimento e Contribuição

Este é um projeto acadêmico e colaborativo vinculado ao NEXT. Se você deseja entender a arquitetura técnica, rodar o projeto localmente ou contribuir com código, acesse nosso guia detalhado:

👉 **[GUIA DE DESENVOLVIMENTO (DEVELOPMENT.md)](./DEVELOPMENT.md)**

---
*Desenvolvido por [Seu Nome] - Núcleo de Estudos em Xadrez & Tecnologias (NEXT)*