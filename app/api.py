from repositories.usuario_repository import UsuarioRepository
from repositories.genero_repository import GeneroRepository
from services.recomendacao_service import RecomendacaoService
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException

class UserAtual:
    def __init__(self):
        self.login=''
        self.adulto=False
        self.nome=''
        self.gen=list()
        
class Login(BaseModel):
    login: str
    senha: str
    
class cadastro(BaseModel):
    nome: str
    login: str
    senha: str
    adulto: bool
    
class Gostos(BaseModel):
    gen_list: list
    
    
user = UserAtual()
app = FastAPI()
recomenda_service = RecomendacaoService()
genero_repo = GeneroRepository()
user_repo = UsuarioRepository()


@app.post('/login')
def login(dados: Login):
    passe = user_repo.autenticar_usuario(dados.login,dados.senha)
    
    if not passe or not passe.get("acesso"):
        raise HTTPException(status_code=401, detail="login inválido")
    
    user.login=dados.login
    
        
    return {'ok': passe['acesso'], 'usuario': passe['login']}

@app.post('/cadastro')
def cadastrar(dados: cadastro):
    passe = user_repo.inserir_usuario(dados.login,dados.nome,dados.senha,dados.adulto)
    
    if not passe[0]:
        raise HTTPException(status_code=401, detail=f"login {passe[1]}")
    
    return True

@app.post('/genero')
def generosTMDB():
    return genero_repo.carregar_generos_tmdb()

@app.post('/salvagostos')
def salvar_generos_usuario(gen_list: Gostos):
    user_repo.associar_generos_usuario(user.login,gen_list.gen_list)
    return True
    
@app.get('/carregargostosusuario')
def carregar_gosto_usuario():
    return genero_repo.buscar_por_usuario(user.login)