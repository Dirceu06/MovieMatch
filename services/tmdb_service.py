import requests
from core.config import Config

class TMDbService:
    def __init__(self):
        self.headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {Config.TMDB_API_KEY}"
        }
    
    def get_generos(self):
        """Busca lista de gêneros do TMDb"""
        url = f"{Config.TMDB_BASE_URL}/genre/movie/list?language=pt"
        response = requests.get(url, headers=self.headers)
        return response.json().get('genres', [])
    
    def discover_movies(self, genero_id=None, page=1, include_adult=False, brasil= False, anoINI=1980, anoFIM=2026):
        """Busca filmes por gênero"""
        url = f"{Config.TMDB_BASE_URL}/discover/movie"
        
        params = {
            "include_adult": False,
            "include_video": False,
            "language": Config.LANGUAGE,
            "page": page,
            "sort_by": "vote_average.desc",
            "vote_count.gte": 300,
            "release_date.gte": f"{anoINI}-01-01",
            "release_date.lte": f"{anoFIM}-12-31"
        }
         
        # params["with_genres"] = genero_id
        if brasil:
            params['with_origin_country'] = 'BR'
        if genero_id:
            params["with_genres"] = genero_id
        
        
        response = requests.get(url, headers=self.headers, params=params)
        return response.json()
    
    def get_movie_details(self, movie_id):
        """Busca detalhes de um filme específico"""
        url = f"{Config.TMDB_BASE_URL}/movie/{movie_id}?language={Config.LANGUAGE}"
        response = requests.get(url, headers=self.headers)
        return response