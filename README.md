# 🎬 MovieMatch - O Tinder dos Filmes

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue.svg)](https://postgresql.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Live Demo](https://img.shields.io/badge/🚀-Live%20Demo-success)](https://moviematch-dejota.streamlit.app)

**MovieMatch** é um sistema de recomendação de filmes com funcionalidades sociais e uma interface intuitiva estilo "Tinder". Descobre o teu próximo filme favorito, avalia sugestões e vê o que os teus amigos estão a assistir.

🔗 **Links Rápidos:** [Live Demo](https://moviematch-dejota.streamlit.app) | [Documentação da API](https://moviematch-6k2e.onrender.com/docs)

> ⚠️ **Nota sobre Performance:** A API está hospedada num serviço gratuito (Render), pelo que a primeira requisição pode demorar alguns segundos a responder (Cold Start). Após a primeira operação, o sistema funciona com a velocidade normal.

## ✨ Funcionalidades

### 🎯 Sistema de Recomendação
- **Match Inteligente:** Recomendações personalizadas baseadas nos teus géneros favoritos.
- **Interface Deslizante:** Estilo Tinder com botões 👍/👎 para avaliar filmes rapidamente.
- **Filtros Avançados:** Filtra por ano, popularidade e destaca **filmes brasileiros**.
- **Dados em Tempo Real:** Integração direta com a API do TMDB.

### 👥 Rede Social
- **Conexões:** Adiciona amigos e acompanha o que eles andam a ver.
- **Match de Amigos:** Descobre filmes em comum que tu e os teus amigos gostaram.
- **Perfil Completo:** Histórico detalhado dos filmes assistidos e avaliados.

### 🔐 Segurança e Arquitetura
- **Autenticação Robusta:** Login seguro com JWT (Access & Refresh Tokens).
- **Proteção de Dados:** Senhas criptografadas com Bcrypt.
- **Arquitetura Modular:** Separação clara entre Frontend (Streamlit) e Backend (FastAPI).

## 🛠️ Tecnologias e Infraestrutura

* **Frontend:** Streamlit (Hospedado na Streamlit Cloud)
* **Backend:** FastAPI (Hospedado no Render - Free Tier)
* **Base de Dados:** PostgreSQL (Hospedado na Neon.tech - Free Tier)

## 📸 Capturas de Ecrã

<div align="center">
  <img src="https://github.com/user-attachments/assets/6ffaafcc-6aca-4d82-beeb-cea9c4a56b5f" width="45%" alt="Tela de Login" />
  <img src="https://github.com/user-attachments/assets/59c52752-53e6-48bf-a542-962a8385369f" width="45%" alt="Tela de Match" />
  <img src="https://github.com/user-attachments/assets/369f3aea-7ead-45fd-be50-2f35afd19170" width="45%" alt="Perfil de Usuário" />
</div>
