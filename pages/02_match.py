import os
import requests
import streamlit as st
from acesso import sair
from core.api_client import rotina_requests
API_URL = st.secrets["API_URL"]
st.set_page_config(page_title='Match',page_icon= ':clapper:',layout='wide')
st.markdown("""
    <style>
        .stMainBlockContainer {
            padding-top: 2rem;
            padding-bottom: 1rem;
            padding-left: 2rem;
            padding-right: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

tamanhos = ['w92','w154','w185','w342','w500','w780']

if "logado" not in st.session_state:    st.session_state.logado = False
if not st.session_state.get("mudouGen"): st.session_state.mudouGen = False
if not st.session_state.get("brasileiro"): st.session_state.brasileiro = False
if not st.session_state.get("sort"): st.session_state.sort = 'popularidade'
if not st.session_state.get("anoInicio"): st.session_state.anoInicio = 1980
if not st.session_state.get("anoFim"): st.session_state.anoFim = 2026
if not st.session_state.get("logado"):  st.switch_page("acesso.py")

if not st.session_state.get("recarregar"): st.session_state.recarregar = False

recarregar = False
def switch_recarregar():
    st.session_state.recarregar = True

def sugestao():
    generos = list()
    for g in st.session_state.genlist:
        generos.append(g)
        
    dados = {
        'login': st.session_state.user['login'],
        'gen': generos,
        'adulto': st.session_state.user['adulto'],
        'brasil': st.session_state.brasileiro,
        'anoINI': st.session_state.anoInicio,
        'anoFIM': st.session_state.anoFim,
        'sort':   st.session_state.sort
    }
    try:
        return rotina_requests('POST','/user/sugestoes',json=dados)
    except RuntimeError:
        sair()

def salvarAvalia(filme_gen,filme_id,filme_aval:bool):
    try:
        rotina_requests('POST',f"/user/avaliar",json={'filme_id': filme_id,'filme_gen': filme_gen,'avaliacao': filme_aval})
    except RuntimeError:
        sair()


if 'filmes' not in st.session_state: st.session_state.filmes = sugestao()

if 'indice' not in st.session_state: st.session_state.indice = 0

# --- FILTROS NO TOPO ---
col_anos, col_sort,col_filtros = st.columns([1, 1, 1])

with col_anos:
    st.markdown("### Filtros")
    st.slider(
        "Intervalo de anos",
        min_value=1930,
        max_value=2026,
        value=(st.session_state.anoInicio, st.session_state.anoFim),
        step=1,
        key="filtro_ano",
        on_change=switch_recarregar
    )
    st.session_state.anoInicio, st.session_state.anoFim = st.session_state.filtro_ano

with col_sort:
    st.space('medium')
    origem = st.selectbox(
        "Organizar por:",
        options=["popularidade", "notas"],
        on_change=switch_recarregar,
        index = 0 if st.session_state.sort == 'popularidade' else 1
    )
    st.session_state.sort = origem

with col_filtros:
    st.space('medium')
    origem = st.selectbox(
        "Origem dos filmes",
        options=["Todos", "Somente brasileiros"],
        on_change=switch_recarregar,
        index= 1 if st.session_state.brasileiro else 0
    )
    st.session_state.brasileiro = (origem == "Somente brasileiros")

if st.session_state.mudouGen or st.session_state.recarregar: 
    st.session_state.filmes = sugestao()
    st.session_state.indice = 0
    st.session_state.mudouGen = False
    st.session_state.recarregar = False

try:
    f=st.session_state.filmes[st.session_state.indice]
    
except IndexError: 
    st.session_state.filmes = sugestao()
    st.session_state.indice = 0
    try: 
        f=st.session_state.filmes[st.session_state.indice]
    except:
        st.space('large')
        st.markdown('## Perdão não achamos filmes com esse filtro',text_alignment='center')
        st.stop()

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
        try:
            del st.session_state.vistos
        except:
            pass
        st.rerun()
with col2:
    if st.button('Gostei ou Pretendo ver', use_container_width=True,on_click=salvarAvalia,args=(f['genre_ids'],f['id'],True)):
        st.session_state.indice += 1
        try:
            del st.session_state.vistos
        except:
            pass
        st.rerun()
            



