from core.databasePB import Database
from psycopg2 import errors
import hashlib
import psycopg2

class UsuarioRepository:
    def __init__(self):
        self.db = Database()
        self.criar_tabelas()
        
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
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuario_amigo (
                login TEXT ,
                login_amigo TEXT ,
                PRIMARY KEY (login, login_amigo),
                FOREIGN KEY (login) REFERENCES usuario(login),
                FOREIGN KEY (login_amigo) REFERENCES usuario(login)
            );
        """)
        
           # Cria a função da trigger
        cursor.execute("""
            CREATE OR REPLACE FUNCTION incrementar_pagina_genero()
            RETURNS TRIGGER AS $$
            DECLARE
                generos_filme INTEGER[];
                genero_id INTEGER;
                contagem INTEGER;
            BEGIN
                -- Busca os gêneros do filme que foi avaliado
                SELECT array_agg(fg.id_genero) INTO generos_filme
                FROM filmes_genero fg
                WHERE fg.id_filme = NEW.id_filme;
                
                -- Para cada gênero do filme
                FOREACH genero_id IN ARRAY generos_filme
                LOOP
                    -- Conta quantos filmes com esse gênero o usuário já avaliou
                    SELECT COUNT(DISTINCT uf.id_filme) INTO contagem
                    FROM usuario_filme uf
                    JOIN filmes_genero fg ON uf.id_filme = fg.id_filme
                    WHERE uf.login = NEW.login
                    AND fg.id_genero = genero_id;
                    
                    -- Se atingiu 20 filmes, incrementa a página
                    IF contagem >= 20 THEN
                        UPDATE usuario_genero_feed
                        SET page = page + 1
                        WHERE login = NEW.login
                        AND id_genero = genero_id;
                    END IF;
                END LOOP;
                
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
        """)
        
        # Cria a trigger
        cursor.execute("""
            DROP TRIGGER IF EXISTS trigger_incrementar_pagina ON usuario_filme;
            CREATE TRIGGER trigger_incrementar_pagina
            AFTER INSERT OR UPDATE ON usuario_filme
            FOR EACH ROW
            EXECUTE FUNCTION incrementar_pagina_genero();
        """)
        self.db.commit()
    
    def inserir_usuario(self, login, nome, senha, adulto):
        """Insere um novo usuário"""
        cursor = self.db.get_cursor()
        
        if (not login or login=='') or (not nome or nome=='') or (not senha or senha==''):
            return [False,'vazio']
        
        cursor.execute("SELECT 1 FROM usuario WHERE login=%s", (login,))
        if cursor.fetchone():
            return [False,'existe']
        
        # CRIPTOGRAFIA AQUI !!!!!!!!!!!!!!!

        cursor.execute("""
            INSERT INTO usuario(login, nome, senha, adulto) 
            VALUES(%s,%s,%s,%s)
        """, (login, nome, senha, adulto))
        
        self.db.commit()
        return [True,'ok']
    
    def autenticar_usuario(self, login, senha):
        """Autentica um usuário"""
        cursor = self.db.get_cursor()
        cursor.execute("SELECT senha FROM usuario WHERE login=%s", (login,))
        
        resultado = cursor.fetchone()
        if not resultado:
            return None
        
        return {'acesso': resultado['senha'] == senha,'login': login }            
    
    def buscar_info_usuario(self, login):
        """Busca informações básicas do usuário"""
        cursor = self.db.get_cursor()
        cursor.execute("SELECT nome, adulto, descricao, perfil_path FROM usuario WHERE login=%s", (login,))
        res = cursor.fetchone()
        return res
    
    def associar_generos_usuario(self, user_id, generos_ids):
        """Associa gêneros a um usuário"""
        cursor = self.db.get_cursor()
        
        try:
            #deleta todos os gêneros anteriores do usuário
            cursor.execute("DELETE FROM usuario_genero WHERE login = %s", (user_id,))
            
            for genero_id in generos_ids:
                try:
                    genero_id = int(genero_id)
                    cursor.execute(
                        "INSERT INTO usuario_genero(login, id_genero) VALUES(%s,%s)",
                        (user_id, genero_id)
                    )
                except ValueError:
                    continue  
                except errors.UniqueViolation:
                    
                    cursor.execute(
                        "INSERT INTO usuario_genero(login, id_genero) VALUES(%s,%s) ON CONFLICT (login, id_genero) DO NOTHING",
                        (user_id, genero_id)
                    )
            
            self.db.commit()
            
        except Exception as e:
            self.db.rollback()  
            raise e  
    
    def get_feed_page(self, user_id, genero_id):
        """Obtém a página atual do feed do usuário para um gênero"""
        cursor = self.db.get_cursor()
        cursor.execute("""
            SELECT page FROM usuario_genero_feed
            WHERE login = %s AND id_genero = %s
        """, (user_id, genero_id))
        
        row = cursor.fetchone()
        if row is not None:
            return row
        
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
        
    def adicionar_amizade(self, user_atual, user_amigo):
        cursor=self.db.get_cursor()
        cursor.execute(
            "SELECT 1 FROM usuario WHERE login=%s",(user_amigo,))
        
        res = cursor.fetchone()
        if res:
            try:
                cursor.execute(
                    "INSERT INTO usuario_amigo(login, login_amigo) values (%s,%s)",(user_atual,user_amigo))
                self.db.commit()
                return [True, 'usuário inserido']
            except:
                self.db.rollback()
                return [False, 'vocês já são amigos']
                
        else:
            return [False, 'amigo inexistente']
        
    def remover_amizade(self, user_atual, user_amigo):
        cursor = self.db.get_cursor()
        cursor.execute(
            "DELETE FROM usuario_amigo WHERE login=%s AND login_amigo=%s",(user_atual,user_amigo))
       
    def lista_amigos(self, user_atual):
        cursor = self.db.get_cursor()
        cursor.execute(
            "SELECT ua.login_amigo, u.nome, u.descricao, u.perfil_path FROM usuario_amigo AS ua JOIN usuario AS u ON u.login=ua.login_amigo WHERE ua.login=%s",(user_atual,))
        lista = cursor.fetchall()
        return lista
    
    def filmes_em_comum(self, user_atual, user_amigo):
        cursor = self.db.get_cursor()

        query = """
            SELECT 
                f.id_filme
            FROM usuario_filme uf1
            JOIN usuario_filme uf2 ON uf1.id_filme = uf2.id_filme
            LEFT JOIN filme f ON uf1.id_filme = f.id_filme
            WHERE uf1.login = %s
            AND uf2.login = %s
            AND uf1.avaliacao = TRUE
            AND uf2.avaliacao = TRUE;
        """
        cursor.execute(query, (user_atual, user_amigo))
        res = cursor.fetchall()
        lista= list()
        
        for r in res: lista.append(r['id_filme'])
        

        return lista