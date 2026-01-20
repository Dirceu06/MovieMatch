from core.config import Config
API_URL = Config.API_URL
import streamlit as st
import requests

st.set_page_config('Inicio', ':clapper:',layout='centered')

if not st.session_state.get("logado"): st.switch_page("acesso.py")



col1, col2 = st.columns([2,4])
with col1:
    st.image(f'assets/perfis/{amigo['perfil_path']}')

with col2: 
    st.title(f'{amigo['nome']}')
    st.caption(f"@{amigo['login_amigo']}")
    st.write(f'{amigo['descricao']}')

st.divider()