from fastapi import APIRouter, HTTPException
from api.schemas import *
from api.api import user_repo

auth_router = APIRouter(prefix='/auth', tags=['auth'])

@auth_router.post('/cadastro')
async def cadastrar(dados: CadastroRequest):
    passe = user_repo.inserir_usuario(dados.login,dados.nome,dados.senha,dados.adulto)
    
    if not passe[0]:
        raise HTTPException(status_code=401, detail=f"login {passe[1]}")
    
    return {'success':True}

@auth_router.post('/login')
async def login(dados: Login):
    passe = user_repo.autenticar_usuario(dados.login,dados.senha)
    
    if not passe or not passe.get("acesso"):
        raise HTTPException(status_code=401, detail="login inválido")
        
    return {'ok': passe['acesso'], 'usuario': passe['login']}

