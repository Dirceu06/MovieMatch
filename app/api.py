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
   
class Avaliar(BaseModel):
    filme_id: int
    filme_gen: list
    login: str
    avaliacao: bool
    
class Relacionamento(BaseModel):
    login: str
    login_amigo: str

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
def infos_user(user: Basico):
    return user_repo.buscar_info_usuario(user.login)

@app.post('/avaliar')
def avaliar(aval: Avaliar):
    recomenda_service.avaliar_filme(aval.login,aval.filme_id,aval.filme_gen,aval.avaliacao)

@app.post('/listaramigos')
def lista_amigos(base: Basico):
    return user_repo.lista_amigos(base.login)

@app.post('/adicionaramigo')
def add_amigo(add: Relacionamento):
    res = user_repo.adicionar_amizade(add.login, add.login_amigo)
    if res[0]:
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": res[1],
                "data": {
                    "login": add.login,
                    "amigo": add.login_amigo
                }
            }
        )
    else:
        # usuario amigo não existe
        return JSONResponse(
            status_code=409,
            content={
                "success": False,
                "message": res[1],
                "data": {
                    "login": add.login,
                    "amigo": add.login_amigo
                }
            }
        )
    
@app.post('/excluiramigo')
def exc_amigo(exc: Relacionamento):
    return user_repo.remover_amizade(exc.login, exc.login_amigo)

@app.post('/filmescomum')
def filmes_iguais(exc: Relacionamento):
    return user_repo.filmes_em_comum(exc.login, exc.login_amigo)