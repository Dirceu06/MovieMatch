import streamlit as st
import requests
from core.config import Config
API_URL = Config.API_URL
st.set_page_config(page_title='acesso',page_icon= ':clapper:',layout='centered')

if "logado" not in st.session_state:
    st.session_state.logado = False

if "rota" not in st.session_state:
    st.session_state.rota = "inicio"
    
if st.session_state.logado:
    st.session_state.rota = 'default'

def sair():
    st.session_state.clear()
    st.cache_data.clear()
    st.switch_page("acesso.py")

def tela_inicio():
    st.title("Bem-vindo",text_alignment='center')

    col1, _,col2 = st.columns([1,0.3,1],vertical_alignment='bottom')

    with col1:
        if st.button("Já tenho conta",width='stretch'):
            st.session_state.rota = "login"
            st.rerun()

    with col2:
        if st.button("Sou novo",width='stretch'):
            st.session_state.rota = "cadastro"
            st.rerun()

def tela_login():
    st.title("Login",text_alignment='center')

    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")
    erro = None
    successo = None
    col1, col2 = st.columns([1,1],vertical_alignment='bottom')
    with col1:
        if st.button("Entrar",width='stretch'):
            resp = requests.post(
                f"{API_URL}/auth/login",
                json={"login": usuario, "senha": senha}
            )

            if resp.status_code == 200:
                st.session_state.logado = True
                login = usuario
                infos =  requests.get(f'{API_URL}/user/infos',json={'login':login}).json()
                nome, adulto = infos['nome'],infos['adulto']
                gen = requests.post(f'{API_URL}/user/carregargostosusuario',json={'login':login}).json()
                genFinal = list()
                for g in gen:
                    genFinal.append(g['id_genero'])
                st.session_state.user = {"nome": nome, "login": login, "adulto": adulto, "gen": genFinal}
                st.switch_page('pages/generos.py')
            else:
                erro="Login inválido"
    with col2:
        if st.button("Voltar",width='stretch'):
            st.session_state.rota = "inicio"
            successo = 'Login válido'
            st.rerun()

    if erro: st.error(erro)
    if successo: st.success(successo)
     
def tela_cadastro():
    st.title("Cadastro",text_alignment='center')

    nome = st.text_input("Nome",placeholder='Zézinho')
    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")
    adulto =  st.checkbox('adulto?',value=False,width='stretch')

    col1, _,col2 = st.columns([1,0.3,1],vertical_alignment='bottom')
    erro = None
    successo = None
    with col1:
        if st.button("Cadastrar",width='stretch'):
            resp = requests.post(
                f"{API_URL}/auth/cadastro",
                json={"login": usuario, "senha": senha, 'nome': nome, 'adulto': adulto}
            )

            if resp.status_code == 200:
                successo =('Usuario criado, faça login')
                st.session_state.rota = 'login'
            else:
                erro = resp.json().get('detail')
                
    with col2:
        if st.button("Voltar",width='stretch'):
            st.session_state.rota = "inicio"
            st.rerun()

    if erro: st.error(erro)
    if successo: st.success(successo)
        
def erro(msg):
    st.error(msg)
    
def tela_default():
    st.title('Bem-Vindo ao Movie Match',text_alignment='center')
    st.subheader('use a barra lateral na esquerda para navegação :smile:', text_alignment='center')
    st.space('medium')
    st.markdown('#### Caso deseje sair:',text_alignment='center')
    _, bt, _ = st.columns([1,1,1])
    with bt:
        if st.button('Logout',width='stretch'):
            sair()

# roteamento manual
if st.session_state.rota == "inicio":
    tela_inicio()
elif st.session_state.rota == "login":
    tela_login()
elif st.session_state.rota == "cadastro":
    tela_cadastro()
elif st.session_state.rota == "default":
    tela_default()