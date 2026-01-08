import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import errors



class Database:
    def __init__(
        self,
        host="localhost",
        database="moviematch",
        user="postgres",
        password="admin",
        port=5432
    ):
        self.config = {
            "host": host,
            "dbname": database,
            "user": user,
            "password": password,
            "port": port,
        }
        self.connection = None

    def connect(self):
        """Estabelece conexão com o PostgreSQL"""
        if not self.connection:
            self.connection = psycopg2.connect(**self.config)
        return self.connection

    def get_cursor(self):
        """Retorna um cursor para execução de queries"""
        return self.connect().cursor(cursor_factory=RealDictCursor)

    def commit(self):
        """Faz commit das alterações"""
        if self.connection:
            self.connection.commit()

    def close(self):
        """Fecha a conexão com o banco"""
        if self.connection:
            self.connection.close()
            self.connection = None
