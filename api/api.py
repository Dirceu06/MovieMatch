from repositories.usuario_repository import UsuarioRepository
from repositories.genero_repository import GeneroRepository
from services.recomendacao_service import RecomendacaoService
from fastapi import FastAPI, HTTPException

app = FastAPI()
recomenda_service = RecomendacaoService()
genero_repo = GeneroRepository()
user_repo = UsuarioRepository()

from api.auth_routes import auth_router
from api.user_routes import user_router


app.include_router(auth_router)
app.include_router(user_router)