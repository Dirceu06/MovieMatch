from core.config import Config
API_URL = Config.API_URL
import streamlit as st
import requests

st.set_page_config('Amizades', ':clapper:', layout='centered')

if not st.session_state.get("logado"): 
    st.switch_page("acesso.py")

@st.cache_data
def buscar_amigos():
    
    response = requests.get(
        f'{API_URL}/listaramigos', 
        json={'login': st.session_state.user['login']},
        timeout=5
    )
    if response.status_code == 200:
        return response.json()
    
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
                        st.switch_page('pages/perfil_amigo.py')
                        
                    if st.button("Excluir",key=f"del_{amigo['nome']}",width='stretch'):
                        ret = requests.post(f"{API_URL}/excluiramigo", 
                            json={'login': st.session_state.user['login'], 'login_amigo': amigo['login_amigo']})
                        
                        st.success(f"Amigo removido!")
                        st.cache_data.clear()
                        st.rerun()

with tab2:
    st.write("### Adicionar amigos")
    
    # Input para buscar
    amigo_login = st.text_input(
        "Digite o login do amigo:",
        key="input_amigo_login"
    )
    
    # Botão de busca
    if st.button("Adicionar amigo", key="btn_buscar"):

        if amigo_login:
            # VALIDAÇÕES
            if amigo_login == st.session_state.user['login']:
                st.error("Você não pode se adicionar!")
            else:
                res = requests.post(f'{API_URL}/adicionaramigo',
                    json={'login': st.session_state.user['login'], 'login_amigo': amigo_login},timeout=5)

                if res.status_code in [200,409]:
                    res = res.json()
                st.write(res)
                if res['success']:
                    st.success(f"{amigo_login} adicionado!")
                    # Limpa o cache e atualiza
                    st.cache_data.clear()
                    st.rerun()
                else:
                    st.error(f'ERRO: {res['message']}')
        else:
            st.warning("Digite um login para buscar")