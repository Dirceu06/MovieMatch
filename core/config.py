import os
class Config:
    # Configurações do TMDb
    TMDB_API_KEY = os.getenv("TMDB_API_KEY")
    TMDB_BASE_URL = "https://api.themoviedb.org/3"
    
    # Configurações do banco
    DB_PATH = "info.db"
    
    # Outras configurações
    LANGUAGE = "pt-BR"
    DEFAULT_PAGE_SIZE = 20
    
    API_URL = "74.220.50.0/24"