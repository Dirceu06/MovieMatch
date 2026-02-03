from core.config import Config
API_URL = Config.API_URL
import streamlit as st
import requests
from core.api_client import rotina_requests

st.set_page_config('Inicio', ':clapper:',layout='centered')

if not st.session_state.get("logado"): st.switch_page("acesso.py")
if not st.session_state.get("mudouGen"): st.session_state.mudouGen = False

if "genlist" not in st.session_state:  st.session_state.genlist = []


def sair():
    st.session_state.clear()
    st.session_state.desconectado = True
    st.cache_data.clear()
    st.switch_page("acesso.py")
    
def buscar_generos():
    try:
        return rotina_requests('GET','/user/genero')
    except RuntimeError:
        sair()
        

@st.cache_data
def carregar_gosto():
    st.session_state.genlist = st.session_state.user['gen']
        
    return st.session_state.user['gen']
   
def salvar_gosto(gen_list: list):
    # requests.post(f'{API_URL}/user/salvagostos',json={'login': st.session_state.user['login'],'gen_list': gen_list}).json()
    try:
        rotina_requests('POST','/user/salvagostos',json={'gen_list': gen_list})
    except RuntimeError:
        sair()
    st.cache_data.clear()
    st.session_state.mudouGen = True
    

# st.sidebar.title("Menu")
# st.sidebar.button("Match",width='stretch',on_click=exibir_opinar_filmes)
# st.sidebar.button("Perfil",width='stretch')
# st.sidebar.markdown("<br>" * 0, unsafe_allow_html=True)
# st.sidebar.button("Logout", width='stretch', on_click=sair)

st.title("seus gêneros de interesse",text_alignment="center",width='stretch')

valores = buscar_generos()
cols = st.columns(3)
 
gostos_atuais = carregar_gosto()

#exibir os generos
for i, genero in enumerate(valores):
    selecionado = genero["id"] in st.session_state.user['gen']
    with cols[i%3]:
        marcado = st.checkbox(
                genero['name'],
                value=selecionado,
                key=f"gen_{genero['id']}"
            )
    if marcado and genero["id"] not in st.session_state.genlist:
        st.session_state.genlist.append(genero["id"])

    if not marcado and genero["id"] in st.session_state.genlist:
        st.session_state.genlist.remove(genero["id"])

st.button('Pronto',width='stretch',on_click=salvar_gosto,args=(st.session_state.genlist,))

