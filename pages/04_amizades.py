from acesso import sair
from core.config import Config
API_URL = Config.API_URL
import streamlit as st
import requests
from core.api_client import rotina_requests

st.set_page_config('Amizades', ':clapper:', layout='centered')

if not st.session_state.get("logado"): 
    st.switch_page("acesso.py")


def buscar_amigos():
    try:
        response = rotina_requests('GET', '/user/listaramigos')
    except RuntimeError:
        sair()
    if len(response) > 0:
        return response
    return None


tab1, tab2 = st.tabs(["Meus Amigos", "Adicionar Amigos"])

with tab1:
    lista_amigos = buscar_amigos()
    
    if not lista_amigos:
        st.info("Você ainda não tem amigos adicionados.")
    else:
        st.write(f"### Você tem {len(lista_amigos)} amigo(s):")
        for amigo in lista_amigos:
            with st.container():
                st.divider()
                col1, col2, col3 = st.columns([1,3, 1])
                
                with col1:
                    st.image('assets/perfis/estatueta.png')
                with col2:
                    st.write(f"**{amigo['nome']}**")
                    st.caption(f"@{amigo['login_amigo']}")
                with col3:
                    if st.button('Detalhes',key=f"detalhes_{amigo['nome']}",width='stretch'):
                        st.session_state.amigo = amigo
                        st.switch_page('pages/05_perfil_amigo.py')
                        
                    if st.button("Excluir",key=f"del_{amigo['nome']}",width='stretch'):
                        try:
                            ret = rotina_requests('POST',f"/user/excluiramigo",json={'login_amigo': amigo['login_amigo']})
                        except RuntimeError:
                            sair()
                        
                        st.success(f"Amigo removido!")
                        st.cache_data.clear()
                        st.rerun()

with tab2:
    st.write("### Adicionar amigos")
    
    amigo_login = st.text_input(
        "Digite o login do amigo:",
        key="input_amigo_login"
    )
    
    if st.button("Adicionar amigo", key="btn_buscar"):

        if amigo_login:
            # VALIDAÇÕES
            if amigo_login == st.session_state.user['login']:
                st.error("Você não pode se adicionar!")
            else:
                try:
                    res = rotina_requests('POST',f'/user/adicionaramigo',json={'login_amigo': amigo_login})
                except RuntimeError:
                    sair()

                if res['success']:
                    st.success(f"{amigo_login} adicionado!")
                    st.cache_data.clear()
                    st.rerun()
                else:
                    st.error(f'ERRO: {res['message']}')
        else:
            st.warning("Digite um login para buscar")