import requests
from core.config import Config
API_URL = Config.API_URL
import streamlit as st

def rotina_requests(method: str, path: str, **kwargs):
    tokens = st.session_state.get("tokens")
    if not tokens:
        raise RuntimeError("Usuário não autenticado")

    headers = kwargs.pop("headers", {})
    headers["Authorization"] = f"Bearer {tokens['access_tk']}"

    resp = requests.request(
        method,
        f"{API_URL}{path}",
        headers=headers,
        **kwargs
    )

    if resp.status_code not in [401, 403, 422, 500, 404, 400]:
        return resp.json()

    # tenta refresh
    refresh = requests.get(
        f"{API_URL}/auth/refresh",
        headers={
            "Authorization": f"Bearer {tokens['refresh_tk']}"
        }
    )

    if refresh.status_code != 200:
        raise RuntimeError("Sessão expirada")

    st.session_state["tokens"] = refresh.json()

    headers["Authorization"] = f"Bearer {st.session_state.tokens['access_tk']}"

    resp = requests.request(
        method,
        f"{API_URL}{path}",
        headers=headers,
        **kwargs
    )

    return resp.json()