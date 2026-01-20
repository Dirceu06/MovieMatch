from core.config import Config
API_URL = Config.API_URL
import streamlit as st
import requests
import math

st.set_page_config('Inicio', ':clapper:',layout='wide')


if not st.session_state.get("logado"): st.switch_page("acesso.py")
if not st.session_state.get('pag_atual'): st.session_state.pag_atual = 0
tamanhos = ['w92','w154','w185','w342','w500','w780']
eu = st.session_state.user


def atualizarInfos(nome, descricao):
    # request.put(f"{API_URL}/user/???", json={'nome': nome, 'descricao': descricao})
    pass

@st.cache_data
def vistos():
    return requests.get(f'{API_URL}/user/idfilmesvistos', json={'login': eu['login']}).json() 

@st.cache_data
def infoFilmes(filmesIds):
    return requests.get(f'{API_URL}/user/infosfilmes',json={'filmes_id': filmesIds}).json()

col1, col2 = st.columns([1,3])
with col1:
    st.image(f'assets/perfis/{eu['perfil_path']}')

with col2: 
    st.text_input(label='Nome', value=f'{eu['nome']}')
    st.caption(f"@{eu['login']}")
    st.text_input(label='Descrição',value=f'{eu['descricao']}')

st.divider()

visto = vistos()

QTDpag = math.ceil(len(visto)/10)
pag_atual = st.session_state.pag_atual

idsAtual = list()
for i in range(0,10):
    idsAtual.append(visto[i+10*pag_atual]['id_filme'])

infos = infoFilmes(idsAtual)

for i in range(0,10):
    f = infos[i]

    col_img, col_info = st.columns([1, 3])
    poster_url = f"https://image.tmdb.org/t/p/{tamanhos[5]}/{f['poster_path']}"
    with col_img:
        st.image(poster_url)

    with col_info:
        st.markdown(f"# {f['title']}")
        col_nota, col_data = st.columns(2)

        with col_nota:
            st.subheader(f"⭐ {f['vote_average']:.1f}/10")
            st.write(f'Com {f['vote_count']} votos')

        with col_data:
            data = f['release_date'].split('-')
            try: st.subheader(f"📅 {data[2]}/{data[1]}/{data[0]}")
            except: st.subheader('sem data')
        st.space(size='small')
        
        st.markdown(f'{f['overview']}')
        generos = ''
        for g in f['genres']:
            generos+=g['name']
            if g!= f['genres'][len(f['genres'])-1]: generos+=', '
            else: generos+='.'
        st.markdown(f'Gêneros: {generos}')

colBt1, colBt2 = st.columns([1,1])
with colBt1:
    if st.button(label='Página anterior', width='stretch'):
        st.session_state.pag_atual-=1
        st.rerun()
with colBt2:
    if st.button(label='Próxima página', width='stretch'):
        st.session_state.pag_atual+=1
        st.rerun()