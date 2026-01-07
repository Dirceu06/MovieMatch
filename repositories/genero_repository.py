from core.databasePB import Database
from services.tmdb_service import TMDbService

class GeneroRepository:
    def __init__(self):
        self.db = Database()
        self.tmdb_service = TMDbService()
    
    def criar_tabela(self):
        """Cria tabela de gêneros se não existir"""
        cursor = self.db.get_cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS genero (
                id_genero INTEGER PRIMARY KEY, 
                nome TEXT 
            )
        """)
        self.db.commit()
    
    def carregar_generos_tmdb(self):
        """Carrega gêneros do TMDb para o banco local"""
        generos = self.tmdb_service.get_generos()
        cursor = self.db.get_cursor()
        
        for genero in generos:
            cursor.execute(
                "INSERT INTO genero(id_genero, nome) VALUES (%s,%s) ON CONFLICT (id_genero) DO NOTHING",
                (genero['id'], genero['name'])
            )
        
        self.db.commit()
        return generos
    
    def buscar_todos(self):
        """Busca todos os gêneros do banco"""
        cursor = self.db.get_cursor()
        cursor.execute("SELECT * FROM genero")
        return cursor.fetchall()
    
    def buscar_por_usuario(self, user_id):
        """Busca gêneros associados a um usuário"""
        cursor = self.db.get_cursor()
        cursor.execute("""
            SELECT g.* FROM genero g
            INNER JOIN usuario_genero ug ON g.id_genero = ug.id_genero
            WHERE ug.login = %s
        """, (user_id,))
        return cursor.fetchall()
    
    def buscar_por_filme(self,filme_id):
        """Busca gêneros associados a um filme"""
        # Fazer
        pass