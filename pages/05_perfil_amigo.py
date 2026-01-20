from core.config import Config
API_URL = Config.API_URL
import streamlit as st
import requests

tamanhos = ['w92','w154','w185','w342','w500','w780']

st.set_page_config('Perfil amigo', ':clapper:', layout='wide')

if not st.session_state.get("logado"): st.switch_page("acesso.py")

if not st.session_state.get('amigo'): st.subheader('Selecione "detalhes" em algum amigo na página amizade',text_alignment='center')
else:
    amigo = st.session_state.amigo

    col1, col2 = st.columns([2,4])
    with col1:
        st.image(f'assets/perfis/{amigo['perfil_path']}')
    
    with col2: 
        st.title(f'{amigo['nome']}')
        st.caption(f"@{amigo['login_amigo']}")
        st.write(f'{amigo['descricao']}')

    st.divider()
    res = requests.get(f"{API_URL}/user/filmescomum",
        json={"login": st.session_state.user['login'], 'login_amigo': amigo['login_amigo']}).json()
    if len(res)!=0:
        st.subheader(f'{len(res)} filmes em comum: ')
        for f in res:
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

    else:
        st.subheader('Parece que vocês não tem filmes em comum')