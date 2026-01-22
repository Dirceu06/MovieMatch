from repositories.usuario_repository import UsuarioRepository
from repositories.filme_repository import FilmeRepository
from repositories.genero_repository import GeneroRepository
from services.tmdb_service import TMDbService

class RecomendacaoService:
    def __init__(self):
        self.genero_repo = GeneroRepository()
        self.filme_repo = FilmeRepository()
        self.usuario_repo = UsuarioRepository()
        self.tmdb_service = TMDbService()
    
    def gerar_sugestoes(self, user_genres, user_id, include_adult:bool, brasil: bool, anoINI, anoFIM, sort):
        """Gera sugestões de filmes baseadas nos gêneros do usuário"""
        vistos = self.filme_repo.buscar_filmes_vistos(user_id)
        
        filmes_excluidos = list()
        for i in vistos:
            filmes_excluidos.append(i['id_filme'])
        filmes_excluidos = set(filmes_excluidos)
        
        lista_intermediaria = list() #cada indice uma lista de 20 por genero
        lista_final = list()
        for genero in user_genres:
            lista_atual = list()
            atendido=False
            try:
                page = self.usuario_repo.get_feed_page(user_id, genero)['page']
            except:
                page=1
            totalPag=1
            while not atendido:
                resultado = self.tmdb_service.discover_movies(
                    genero_id=genero,
                    page=page,
                    include_adult=include_adult,
                    brasil=brasil,
                    anoINI=anoINI,
                    anoFIM=anoFIM,
                    sort=sort
                )
                filmes = resultado.get("results", [])
                qtdPage= resultado.get('total_pages')
                totalPag = qtdPage
                # for filme in filmes:
                for filme in filmes:
                    if filme['overview'] == '': continue
                    if filme["id"] not in filmes_excluidos:
                        lista_atual.append(filme)
                        filmes_excluidos.add(filme["id"])
                    
                if len(lista_atual)>=20 or page > totalPag:
                    atendido=True          
                else: 
                    page = page + 1
            lista_intermediaria.append(lista_atual)
        
        for i in range(0,20):
            for j in range(0,len(lista_intermediaria)):
                if len(lista_final)>=20: break
                try:
                    lista_final.append(lista_intermediaria[j][i])
                except IndexError:
                    continue
        
        return lista_final
    
    def avaliar_filme(self, user_id, filme_id, filme_generos, opiniao):
        """Registra avaliação de um filme"""
        # Insere filme e associa gêneros
        self.filme_repo.inserir_filme(filme_id)
        self.filme_repo.associar_generos_filme(filme_id, filme_generos)
        
        # Registra avaliação do usuário
        self.filme_repo.registrar_avaliacao(user_id, filme_id, opiniao)

    def carrgar_filmes_infos(self, IDs: list):
        carrosel = list()
        for id in IDs:
            filmeInfo = self.tmdb_service.get_movie_details(id)
            if filmeInfo.status_code == 200:
                carrosel.append(filmeInfo.json())
        return carrosel