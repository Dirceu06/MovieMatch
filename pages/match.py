import requests
import streamlit as st
from core.config import Config
API_URL = Config.API_URL
st.set_page_config(page_title='Match',page_icon= ':clapper:',layout='wide')

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
    
    return requests.post(f'{API_URL}/sugestoes', json=dados)

lista = sugestao().json()
tamanhos = ['w92','w154','w185','w342','w500','w780']

for f in lista:
    poster_url = f'https://image.tmdb.org/t/p/{tamanhos[5]}/{f['poster_path']}'

    col_img, col_info = st.columns([1, 3],width='stretch')

    with col_img:
        st.image(poster_url)
        
    with col_info:
        # linha 1 – título
        st.markdown(f"# {f['title']}")

        # linha 2 – nota + data
        col_nota, col_data = st.columns(2)

        with col_nota:
            st.subheader(f"⭐ {f['vote_average']:.1f}/10 com {f['vote_count']} avaliações")

        with col_data:
            data = f['release_date'].split('-')
            st.subheader(f"📅 {data[2]}/{data[1]}/{data[0]}")
            
        st.markdown(f'{f['overview']}')