from repositories.usuario_repository import UsuarioRepository
from repositories.genero_repository import GeneroRepository
from services.recomendacao_service import RecomendacaoService
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException

class Basico(BaseModel):
    login: str

class Basico2(BaseModel):
    login: str
    gen: list
    adulto: bool
    
class Login(BaseModel):
    login: str
    senha: str
    
class cadastro(BaseModel):
    nome: str
    login: str
    senha: str
    adulto: bool
    
class Gostos(BaseModel):
    login: str
    gen_list: list
    
app = FastAPI()
recomenda_service = RecomendacaoService()
genero_repo = GeneroRepository()
user_repo = UsuarioRepository()

@app.post('/login')
def login(dados: Login):
    passe = user_repo.autenticar_usuario(dados.login,dados.senha)
    
    if not passe or not passe.get("acesso"):
        raise HTTPException(status_code=401, detail="login inválido")
        
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
    print(gen_list)
    try:
        user_repo.associar_generos_usuario(gen_list.login, gen_list.gen_list)
        return JSONResponse(content={"success": True, "message": "Gêneros salvos com sucesso"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao salvar gêneros: {str(e)}")
    
@app.post('/carregargostosusuario')
def carregar_gosto_usuario(user: Basico):
    resultado= genero_repo.buscar_por_usuario(user.login)
    res = list()
    for r in resultado:
        res.append(r['id_genero'])
    return resultado

@app.post('/sugestoes')
def carregar_sugestoes(user:Basico2):
    return recomenda_service.gerar_sugestoes(user.gen,user.login,user.adulto)

@app.post('/infos')
def infosUser(user: Basico):
    return user_repo.buscar_info_usuario(user.login)