from core.config import Config
API_URL = Config.API_URL
import streamlit as st
import requests

st.set_page_config('Amizades', ':clapper:', layout='centered')

if not st.session_state.get("logado"): 
    st.switch_page("acesso.py")

@st.cache_data
def buscar_amigos():
    
    response = requests.post(
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
    # if st.button('again'):
    #     buscar_amigos.clear()
    #     lista_amigos = buscar_amigos()

    # st.write(lista_amigos)
    
    if not lista_amigos:
        st.info("Você ainda não tem amigos adicionados.")
    else:
        st.write(f"### Você tem {len(lista_amigos)} amigo(s):")
        for amigo in lista_amigos:
            with st.container():
                st.divider()
                col1, col2, col3 = st.columns([1,3, 1])
                
                filmes_comum = requests.post(f'{API_URL}/filmescomum', json={'login': st.session_state.user['login'], 'login_amigo': amigo['login_amigo']}).json()

                with col1:
                    st.image('https://cdn-icons-png.flaticon.com/512/1144/1144760.png')
                with col2:
                    st.write(f"**{amigo['nome']}**")
                    if filmes_comum is not None:
                        st.write(f'Vocês tem {len(filmes_comum)} em comum')
                    else: 
                        st.write('Vocês não tem filmes em comum')
                    st.caption(f"@{amigo['login_amigo']}")
                with col3:
                    if st.button("Excluir",key=f"del_{amigo['nome']}",width='stretch'):
                        ret = requests.post(f"{API_URL}/excluiramigo", 
                            json={'login': st.session_state.user['login'], 'login_amigo': amigo['login_amigo']})
                        
                        st.success(f"Amigo removido!")
                        st.cache_data.clear()
                        st.rerun()

with tab2:
    st.write("### Buscar e adicionar amigos")
    
    # Input para buscar
    amigo_login = st.text_input(
        "Digite o login do amigo:",
        key="input_amigo_login"
    )
    
    # Botão de busca
    if st.button("🔍 Buscar Usuário", key="btn_buscar"):
        if amigo_login:
            # VALIDAÇÕES
            if amigo_login == st.session_state.user['login']:
                st.error("Você não pode se adicionar!")
            else:
                # SIMULA BUSCA (substitua pela API real)
                st.write(f"### Resultados para '{amigo_login}':")
                
                # Exemplo de resultado
                resultado = {
                    "login": amigo_login,
                    "nome": f"Usuário {amigo_login}",
                    "encontrado": True
                }
                
                if resultado["encontrado"]:
                    st.divider()
                    col_info, col_add = st.columns([3, 1])
                    with col_info:
                        st.write(f"**Nome:** {resultado['nome']}")
                        st.write(f"**Login:** {resultado['login']}")
                    with col_add:
                        if st.button("➕ Adicionar", key=f"add_{resultado['login']}"):
                            # API call para adicionar
                            # response = requests.post(...)
                            st.success(f"{resultado['nome']} adicionado!")
                            # Limpa o cache e atualiza
                            st.cache_data.clear()
                            amigo_login = ""  # Limpa o input
                            st.rerun()
                else:
                    st.error("Usuário não encontrado!")
        else:
            st.warning("Digite um login para buscar")