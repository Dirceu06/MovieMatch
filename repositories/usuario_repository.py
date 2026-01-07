from core.databasePB import Database

class UsuarioRepository:
    def __init__(self):
        self.db = Database()
    
    def criar_tabelas(self):
        """Cria todas as tabelas relacionadas a usuários"""
        cursor = self.db.get_cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuario (
                login TEXT PRIMARY KEY,
                nome TEXT ,
                senha TEXT ,
                adulto BOOLEAN
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuario_genero (
                id_genero INTEGER, 
                login TEXT ,
                PRIMARY KEY (login, id_genero),
                FOREIGN KEY (id_genero) REFERENCES genero(id_genero),
                FOREIGN KEY (login) REFERENCES usuario(login)
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuario_genero_feed (
                login TEXT,
                id_genero INTEGER,
                page INTEGER DEFAULT 1,
                PRIMARY KEY (login, id_genero),
                FOREIGN KEY (login) REFERENCES usuario(login),
                FOREIGN KEY (id_genero) REFERENCES genero(id_genero)
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuario_filme (
                login TEXT ,
                id_filme INTEGER,
                avaliacao BOOLEAN,
                PRIMARY KEY (login, id_filme),
                FOREIGN KEY (login) REFERENCES usuario(login),
                FOREIGN KEY (id_filme) REFERENCES filme(id_filme)
            );
        """)
        
        self.db.commit()
    
    def inserir_usuario(self, login, nome, senha, adulto):
        """Insere um novo usuário"""
        cursor = self.db.get_cursor()
        
        cursor.execute("SELECT 1 FROM usuario WHERE login=%s", (login,))
        if cursor.fetchone():
            return False
        
        cursor.execute("""
            INSERT INTO usuario(login, nome, senha, adulto) 
            VALUES(%s,%s,%s,%s)
        """, (login, nome, senha, adulto))
        
        self.db.commit()
        return True
    
    def autenticar_usuario(self, login, senha):
        """Autentica um usuário"""
        cursor = self.db.get_cursor()
        cursor.execute("SELECT senha FROM usuario WHERE login=%s", (login,))
        
        resultado = cursor.fetchone()
        if not resultado:
            return False
        
        return resultado[0] == senha
    
    def buscar_info_usuario(self, login):
        """Busca informações básicas do usuário"""
        cursor = self.db.get_cursor()
        cursor.execute("SELECT nome, adulto FROM usuario WHERE login=%s", (login,))
        return cursor.fetchone()
    
    def associar_generos_usuario(self, user_id, generos_ids):
        """Associa gêneros a um usuário"""
        cursor = self.db.get_cursor()
        
        for genero_id in generos_ids:
            try:
                genero_id = int(genero_id)
                cursor.execute(
                    "INSERT into usuario_genero(login, id_genero) VALUES(%s,%s) ON CONFLICT (login, id_genero) DO NOTHING",
                    (user_id, genero_id)
                )
            except ValueError:
                continue
        
        self.db.commit()
    
    def get_feed_page(self, user_id, genero_id):
        """Obtém a página atual do feed do usuário para um gênero"""
        cursor = self.db.get_cursor()
        cursor.execute("""
            SELECT page FROM usuario_genero_feed
            WHERE login = %s AND id_genero = %s
        """, (user_id, genero_id))
        
        row = cursor.fetchone()
        if row:
            return row[0]
        
        # Se não existir, cria registro com página 1
        cursor.execute("""
            INSERT INTO usuario_genero_feed (login, id_genero, page)
            VALUES (%s, %s, 1)
        """, (user_id, genero_id))
        
        self.db.commit()
        return 1
    
    def avancar_feed_page(self, user_id, genero_id):
        """Avança a página do feed do usuário para um gênero"""
        cursor = self.db.get_cursor()
        cursor.execute("""
            UPDATE usuario_genero_feed
            SET page = page + 1
            WHERE login = %s AND id_genero = %s
        """, (user_id, genero_id))
        self.db.commit()