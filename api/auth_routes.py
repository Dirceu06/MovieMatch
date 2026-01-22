from fastapi import APIRouter, HTTPException
from api.schemas import *
from api.api import auth_service

auth_router = APIRouter(prefix='/auth', tags=['auth'])

@auth_router.post('/cadastro')
async def cadastrar(dados: CadastroRequest):
    """Rota para cadastrar um novo usuário"""
    ok, msg = auth_service.cadastrar_usuario(
        dados.login, dados.nome, dados.senha
    )
    if not ok:
        raise HTTPException(status_code=400, detail=msg)

    return {"mensagem": msg}

@auth_router.post('/login')
async def login(dados: Login):
    """Rota para autenticar um usuário"""
    if not auth_service.autenticar_usuario(dados.login, dados.senha):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    return {"login": dados.login, "acesso": True}       

