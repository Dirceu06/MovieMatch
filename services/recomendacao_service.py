from repositories.usuario_repository import UsuarioRepository
from repositories.filme_repository import FilmeRepository
from repositories.genero_repository import GeneroRepository
from services.tmdb_service import TMDbService

class RecomendacaoService:
    def __init__(self):
        self.usuario_repo = UsuarioRepository()
        self.filme_repo = FilmeRepository()
        self.genero_repo = GeneroRepository()
        self.tmdb_service = TMDbService()
    
    def gerar_sugestoes(self, user_genres, user_id, include_adult, limite=20):
        """Gera sugestões de filmes baseadas nos gêneros do usuário"""
        filmes_vistos = set(self.filme_repo.buscar_filmes_vistos(user_id))
        sugestoes = []
        
        for genero in user_genres:
            genero_id = genero[0]
            page = self.usuario_repo.get_feed_page(user_id, genero_id)
            
            # Busca filmes do TMDb
            resultado = self.tmdb_service.discover_movies(
                genero_id=genero_id,
                page=page,
                include_adult=include_adult
            )
            
            filmes = resultado.get("results", [])
            
            # Filtra filmes não vistos
            for filme in filmes:
                if filme["id"] not in filmes_vistos:
                    sugestoes.append(filme)
                    filmes_vistos.add(filme["id"])
                    
                    if len(sugestoes) >= limite:
                        break
            
            # Avança página se necessário
            if len(filmes) == 20:  # Página cheia
                self.usuario_repo.avancar_feed_page(user_id, genero_id)
            
            if len(sugestoes) >= limite:
                break
        
        return sugestoes
    
    def avaliar_filme(self, user_id, filme_id, filme_generos, opiniao):
        """Registra avaliação de um filme"""
        # Insere filme e associa gêneros
        self.filme_repo.inserir_filme(filme_id)
        self.filme_repo.associar_generos_filme(filme_id, filme_generos)
        
        # Registra avaliação do usuário
        self.filme_repo.registrar_avaliacao(user_id, filme_id, opiniao)