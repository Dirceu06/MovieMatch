import os
from repositories.usuario_repository import UsuarioRepository
from repositories.genero_repository import GeneroRepository
from repositories.filme_repository import FilmeRepository
from services.recomendacao_service import RecomendacaoService
from services.auth_service import AuthService
from fastapi import FastAPI

algorithm = os.getenv("ALGORITHM")
access_token_expire_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
secret_key = os.getenv("SECRET_KEY")

app = FastAPI()
recomenda_service = RecomendacaoService()
genero_repo = GeneroRepository()
user_repo = UsuarioRepository()
filme_repo = FilmeRepository()
auth_service = AuthService(user_repo)

from api.auth_routes import auth_router
from api.user_routes import user_router


app.include_router(auth_router)
app.include_router(user_router)