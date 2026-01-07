import streamlit as st
st.set_page_config('Inicio', ':clapper:')

if not st.session_state.get("logado"):
    st.switch_page("acesso.py")

st.sidebar.title("Menu")

st.sidebar.button("Dashboard",width='stretch')
st.sidebar.button("Perfil",width='stretch')

# empurra tudo pra cima
st.sidebar.markdown("<br>" * 8, unsafe_allow_html=True)

if st.sidebar.button("Logout", width='stretch'):
    st.session_state.clear()
    st.switch_page("acesso.py")


st.title("Dashboard")
st.write("Área protegida")
