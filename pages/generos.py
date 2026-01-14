from core.config import Config
API_URL = Config.API_URL
import streamlit as st
import requests

st.set_page_config('Inicio', ':clapper:',layout='centered')

if not st.session_state.get("logado"): st.switch_page("acesso.py")
if "genlist" not in st.session_state:  st.session_state.genlist = []

def exibir_opinar_filmes():
    st.success('deu em')

def sair():
    st.session_state.clear()
    st.cache_data.clear()
    st.switch_page("acesso.py")
    
@st.cache_data
def buscar_generos():
    return requests.get(f'{API_URL}/genero').json()

@st.cache_data
def carregar_gosto():
    st.session_state.genlist = st.session_state.user['gen']
        
    return st.session_state.user['gen']
   
def salvar_gosto(gen_list: list):
    requests.post(f'{API_URL}/salvagostos',json={'login': st.session_state.user['login'],'gen_list': gen_list}).json()
    st.cache_data.clear()
    if "mudou_gen" not in st.session_state: st.session_state.mudou_gen = True
    st.session_state.mudou_gen = True
    

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

