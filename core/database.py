import sqlite3

class Database:
    def __init__(self, db_path="info.db"):
        self.db_path = db_path
        self.connection = None
        
    def connect(self):
        """Estabelece conexão com o banco de dados"""
        if not self.connection:
            self.connection = sqlite3.connect(
                self.db_path,
                check_same_thread=False
            )
            self.connection.execute("PRAGMA foreign_keys = ON;")
        return self.connection
    
    def get_cursor(self):
        """Retorna um cursor para execução de queries"""
        return self.connect().cursor()
    
    def commit(self):
        """Faz commit das alterações"""
        if self.connection:
            self.connection.commit()
    
    def close(self):
        """Fecha a conexão com o banco"""
        if self.connection:
            self.connection.close()