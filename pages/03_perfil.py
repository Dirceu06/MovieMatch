import os
from acesso import sair
API_URL = st.secrets["API_URL"]
import streamlit as st
import requests
import math
from core.api_client import rotina_requests

st.set_page_config('Inicio', ':clapper:',layout='wide')

if not st.session_state.get("logado"): st.switch_page("acesso.py")
if not st.session_state.get('pag_atual'): st.session_state.pag_atual = 0
tamanhos = ['w92','w154','w185','w342','w500','w780']
eu = st.session_state.user

def atualizarInfos(nome, descricao):
    try:
        res = rotina_requests('PATCH', '/user/atualizainfos', json={'nome': nome, 'descricao': descricao, 'login': eu['login']})
    except RuntimeError:
        sair()
    return res['success'] if 'success' in res else False
    
def vistos():
    try:
        return rotina_requests('GET', '/user/idfilmesvistos')
    except RuntimeError:
        sair()

if 'vistos' not in st.session_state:
    st.session_state.vistos = vistos()

@st.cache_data
def infoFilmes(filmesIds):
    return requests.get(f'{API_URL}/user/infosfilmes',json={'filmes_id': filmesIds}).json()

col1, col2 = st.columns([1,3])
with col1:
    st.image(f'assets/perfis/{eu['perfil_path']}')

with col2:
    nome = st.text_input(label='Nome', value=f'{eu['nome']}', key='input_nome')
    st.caption(f"@{eu['login']}")
    descricao = st.text_input(label='Descrição', value=f'{eu['descricao']}', key='input_descricao')
    
    if nome != eu['nome'] or descricao != eu['descricao']:
        if st.button(label='Salvar', width='stretch'):
            if atualizarInfos(nome, descricao):
                eu['nome'], eu['descricao'] = nome, descricao
            st.success('Informações atualizadas!')
            st.rerun()

st.divider()

visto = st.session_state.vistos

if len(visto) == 0:
    st.warning('Você ainda não marcou nenhum filme como visto. Vá até a página de recomendações e comece a explorar!')
    st.stop()
else:
    st.subheader(f'Você já viu {len(visto)} filmes!')

QTDpag = math.ceil(len(visto)/10)
pag_atual = st.session_state.pag_atual

idsAtual = list()
for i in range(0,10):
    try:
        idsAtual.append(visto[i+10*pag_atual]['id_filme'])
    except:
        break

infos = infoFilmes(idsAtual)

for i in range(0,10):
    try:
        f = infos[i]
    except:
        break

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
    if pag_atual!=0:
        if st.button(label='Página anterior', width='stretch'):
            st.session_state.pag_atual-=1
            st.rerun()
with colBt2:
    if pag_atual < QTDpag-1:
        if st.button(label='Próxima página', width='stretch'):
            st.session_state.pag_atual+=1
            st.rerun()