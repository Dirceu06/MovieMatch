from core.databasePB import Database

class FilmeRepository:
    def __init__(self):
        self.db = Database()
    
    def criar_tabelas(self):
        """Cria tabelas relacionadas a filmes"""
        cursor = self.db.get_cursor()
        
        cursor.executescript("""
            CREATE TABLE IF NOT EXISTS filme (
                id_filme INTEGER PRIMARY KEY
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS filmes_genero (
                id_genero INTEGER, 
                id_filme INTEGER ,
                PRIMARY KEY (id_filme, id_genero),
                FOREIGN KEY (id_genero) REFERENCES genero(id_genero),
                FOREIGN KEY (id_filme) REFERENCES filme(id_filme)
            );
        """)
        
        self.db.commit()
    
    def inserir_filme(self, filme_id):
        """Insere um filme no banco"""
        cursor = self.db.get_cursor()
        cursor.execute(
            "INSERT INTO filme(id_filme) VALUES(%s) on conflict (id_filme) do nothing",
            (filme_id,)
        )
        self.db.commit()
    
    def associar_generos_filme(self, filme_id, generos_ids):
        """Associa gêneros a um filme"""
        cursor = self.db.get_cursor()
        
        for genero_id in generos_ids:
            cursor.execute(
                "INSERT INTO filmes_genero(id_filme, id_genero) VALUES (%s,%s) on conflict (id_filme, id_genero) do nothing",
                (filme_id, genero_id)
            )
        
        self.db.commit()
    
    def registrar_avaliacao(self, user_id, filme_id, avaliacao):
        """Registra avaliação de um filme por um usuário"""
        cursor = self.db.get_cursor()
        cursor.execute("""
            INSERT INTO usuario_filme(login, id_filme, avaliacao)
            VALUES (%s,%s,%s)
            ON CONFLICT (login,id_filme)
            DO UPDATE SET
                login = EXCLUDED.login,
                id_filme = EXCLUDED.id_filme,
                avaliacao = EXCLUDED.avaliacao;
        """, (user_id, filme_id, avaliacao))
        self.db.commit()
    
    def buscar_filmes_vistos(self, user_id):
        """Busca filmes já vistos pelo usuário"""
        cursor = self.db.get_cursor()
        cursor.execute(
            "SELECT id_filme FROM usuario_filme WHERE login = %s",
            (user_id,)
        )
        
        return [row[0] for row in cursor.fetchall()]