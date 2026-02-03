from fastapi import APIRouter, HTTPException, Header
from api.schemas import *
from api.api import auth_service, algorithm, access_token_expire_minutes, secret_key
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone

auth_router = APIRouter(prefix='/auth', tags=['auth'])

def criar_token(id_usuario, duracao = timedelta(minutes = access_token_expire_minutes)):
    """Função para criar um token de autenticação"""
    data_expiracao = datetime.now(timezone.utc) + duracao
    dicInfo = {'sub': id_usuario, "exp": data_expiracao}
    jwt_cod = jwt.encode(dicInfo, key=secret_key, algorithm= algorithm)
    return jwt_cod

@auth_router.get('/verificatokens')
def verificar_token(token: str):
    """Função para verificar um token de autenticação"""
    try:
        infos = jwt.decode(token, key=secret_key, algorithms=[algorithm])
        exp_time = infos['exp']
        is_valid = exp_time > datetime.now(timezone.utc).timestamp()
        return {
            "valido": is_valid,
            "usuario": infos['sub'],
            "expiracao": exp_time
        }
    except JWTError:
        return {"valido": False, "erro": "Token inválido"}
    
@auth_router.get("/refresh")
def atualizar_tokens(authorization: str = Header(...)):
    """Função para renovar um token de autenticação"""
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Header inválido")

    rf_token = authorization.removeprefix("Bearer ").strip()
    dados = verificar_token(rf_token)
    if not dados['valido']:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")

    novo_token = criar_token(dados['usuario'])
    return {'access_tk': novo_token, "refresh_tk": rf_token}


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

    acess_tk = criar_token(dados.login, timedelta(minutes=30))
    refresh_tk = criar_token(dados.login, timedelta(days=7)) 
    return {'access_tk': acess_tk, "refresh_tk": refresh_tk}

