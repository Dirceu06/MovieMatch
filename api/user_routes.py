from fastapi import APIRouter, HTTPException, Depends
from api.schemas import *
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from api.auth_routes import verificar_token
from api.api import  recomenda_service, genero_repo, user_repo, filme_repo

user_router = APIRouter(prefix='/user', tags=['user'])

security = HTTPBearer()

def get_usuario(
    cred: HTTPAuthorizationCredentials = Depends(security)
):
    token = cred.credentials

    dados = verificar_token(token)
    if not dados["valido"]:
        raise HTTPException(status_code=401)
    
    return dados["usuario"]

@user_router.get('/genero')
async def generosTMDB():
    return genero_repo.carregar_generos_tmdb()

@user_router.post('/salvagostos')
async def salvar_generos_usuario(gen_list: Gostos, usuario: str = Depends(get_usuario)):
    try:
        user_repo.associar_generos_usuario(usuario, gen_list.gen_list)
        return JSONResponse(content={"success": True, "message": "Gêneros salvos com sucesso"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao salvar gêneros: {str(e)}")
    
@user_router.post('/carregargostosusuario')
async def carregar_gosto_usuario(usuario: str = Depends(get_usuario)):
    resultado= genero_repo.buscar_por_usuario(usuario)
    return resultado

@user_router.post('/sugestoes')
async def carregar_sugestoes(user:SugestaoRequest, usuario: str = Depends(get_usuario)):
    resp = recomenda_service.gerar_sugestoes(user.gen,user.login,user.adulto, user.brasil, user.anoINI, user.anoFIM, user.sort)
    return resp

@user_router.get('/infos')
async def infos_user(usuario: str = Depends(get_usuario)):
    return user_repo.buscar_info_usuario(usuario)

@user_router.post('/avaliar')
async def avaliar(aval: Avaliar, usuario: str = Depends(get_usuario)):
    recomenda_service.avaliar_filme(usuario,aval.filme_id,aval.filme_gen,aval.avaliacao)
    return {"success": True}

@user_router.get('/listaramigos')
async def lista_amigos(usuario: str = Depends(get_usuario)):
    return user_repo.lista_amigos(usuario)

@user_router.post('/adicionaramigo')
async def add_amigo(add: Relacionamento, usuario: str = Depends(get_usuario)):
    res = user_repo.adicionar_amizade(usuario, add.login_amigo)
    if res[0]:
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": res[1],
                "data": {
                    "login": usuario,
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
                    "login": usuario,
                    "amigo": add.login_amigo
                }
            }
        )
    
@user_router.post('/excluiramigo')
async def exc_amigo(exc: Relacionamento, usuario: str = Depends(get_usuario)):
    return user_repo.remover_amizade(usuario, exc.login_amigo)

@user_router.get('/filmescomum')
async def filmes_iguais(exc: Relacionamento, usuario: str = Depends(get_usuario)):
    filmesComum =  user_repo.filmes_em_comum(usuario, exc.login_amigo)
    res = recomenda_service.carrgar_filmes_infos(filmesComum)
    return res

@user_router.get('/idfilmesvistos')
async def filmes_vistos(usuario: str = Depends(get_usuario)):
    listaVistos = filme_repo.buscar_filmes_vistos(usuario)
    return listaVistos

@user_router.get('/infosfilmes')
async def infos_filmes(filmes: FilmesIdsRequests):
    infosVistos = recomenda_service.carrgar_filmes_infos(filmes.filmes_id)
    return infosVistos

@user_router.patch('/atualizainfos')
async def atualizar_infos(infos: InfosChangeRequests, usuario: str = Depends(get_usuario)):
    user_repo.alterar_usuario(infos.nome, infos.descricao, infos.login)
    return {"success": True}

@user_router.patch('/atualizaperfil')
async def atualizar_perfil_infos(infos: PerfilChangeRequests, usuario: str = Depends(get_usuario)):
    user_repo.alterar_perfil_usuario(infos.caminho, infos.login)
    