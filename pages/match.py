import requests
import streamlit as st
from core.config import Config
API_URL = Config.API_URL
st.set_page_config(page_title='Match',page_icon= ':clapper:',layout='wide')

tamanhos = ['w92','w154','w185','w342','w500','w780']

if "logado" not in st.session_state:    st.session_state.logado = False
    
if not st.session_state.get("logado"):  st.switch_page("acesso.py")

def sugestao():
    generos = list()
    for g in st.session_state.genlist:
        generos.append(g)
        
    dados = {
        'login': st.session_state.user['login'],
        'gen': generos,
        'adulto': st.session_state.user['adulto']
    }

    return requests.post(f'{API_URL}/sugestoes', json=dados).json()

def salvarAvalia(filme_gen,filme_id,filme_aval:bool):
    requests.post(f"{API_URL}/avaliar",json={'filme_id': filme_id,'filme_gen': filme_gen,'avaliacao': filme_aval, 'login': st.session_state.user['login']})


if 'filmes' not in st.session_state: st.session_state.filmes = sugestao()

if 'indice' not in st.session_state: st.session_state.indice = 0


try:
    f=st.session_state.filmes[st.session_state.indice]
    
    
except IndexError:
    
    st.session_state.filmes = sugestao()
    st.session_state.indice = 0
    f=st.session_state.filmes[st.session_state.indice]
    
poster_url = f'https://image.tmdb.org/t/p/{tamanhos[5]}/{f['poster_path']}'

col_img, col_info = st.columns([1, 3])

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
    
col1, col2 = st.columns([1,1])
with col1:
    if st.button('Não gostei', use_container_width=True,on_click=salvarAvalia,args=(f['genre_ids'],f['id'],False)):
        st.session_state.indice += 1
        st.rerun()
with col2:
    if st.button('Gostei ou Pretendo ver', use_container_width=True,on_click=salvarAvalia,args=(f['genre_ids'],f['id'],True)):
        st.session_state.indice += 1
        st.rerun()
        