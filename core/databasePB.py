import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import errors
import os
from dotenv import load_dotenv

# CARREGUE AS VARIÁVEIS DE AMBIENTE AQUI, NO TOPO DO ARQUIVO
load_dotenv()

class Database:
    def __init__(
        self,
        host=None,
        database=None,
        user=None,
        password=None,
        port=None
    ):
        self.config = {
            'host':os.getenv("DB_HOST"),
            'database':os.getenv("DB_NAME"),
            'user':os.getenv("DB_USER"),
            'password':os.getenv("DB_PASSWORD"),
            'port':os.getenv("DB_PORT")
            
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
