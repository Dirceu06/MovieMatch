from fastapi import APIRouter, HTTPException
from api.schemas import *
from fastapi.responses import JSONResponse

from api.api import  recomenda_service, genero_repo, user_repo

user_router = APIRouter(prefix='/user', tags=['user'])

@user_router.get('/genero')
async def generosTMDB():
    return genero_repo.carregar_generos_tmdb()

@user_router.post('/salvagostos')
async def salvar_generos_usuario(gen_list: Gostos):
    try:
        user_repo.associar_generos_usuario(gen_list.login, gen_list.gen_list)
        return JSONResponse(content={"success": True, "message": "Gêneros salvos com sucesso"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao salvar gêneros: {str(e)}")
    
@user_router.post('/carregargostosusuario')
async def carregar_gosto_usuario(user: UserRequest):
    resultado= genero_repo.buscar_por_usuario(user.login)
    res = list()
    for r in resultado:
        res.append(r['id_genero'])
    return resultado

@user_router.post('/sugestoes')
async def carregar_sugestoes(user:SugestaoRequest):
    resp = recomenda_service.gerar_sugestoes(user.gen,user.login,user.adulto, user.brasil, user.anoINI, user.anoFIM, user.sort)
    return resp

@user_router.get('/infos')
async def infos_user(user: UserRequest):
    return user_repo.buscar_info_usuario(user.login)

@user_router.post('/avaliar')
async def avaliar(aval: Avaliar):
    recomenda_service.avaliar_filme(aval.login,aval.filme_id,aval.filme_gen,aval.avaliacao)
    return {"success": True}

@user_router.get('/listaramigos')
async def lista_amigos(base: UserRequest):
    return user_repo.lista_amigos(base.login)

@user_router.post('/adicionaramigo')
async def add_amigo(add: Relacionamento):
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
    
@user_router.post('/excluiramigo')
async def exc_amigo(exc: Relacionamento):
    return user_repo.remover_amizade(exc.login, exc.login_amigo)

@user_router.get('/filmescomum')
async def filmes_iguais(exc: Relacionamento):
    filmesComum =  user_repo.filmes_em_comum(exc.login, exc.login_amigo)
    res = recomenda_service.carrgar_filmes_infos(filmesComum)
    return res