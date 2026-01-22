import bcrypt

class AuthService:
    def __init__(self, user_repo):
        self.user_repo = user_repo

    def cadastrar_usuario(self, login, nome, senha):
        """Cadastra um novo usuário"""
        try:
            hash_senha = self._hash_senha(senha)
            hash_str = hash_senha.decode("utf-8")
            self.user_repo.inserir_usuario(login, nome, hash_str)
        except ValueError as e:
            return False, str(e)
        return True, "Usuário cadastrado com sucesso"
    
    def autenticar_usuario(self, login, senha):
        """Autentica um usuário"""
        senha_hash = self.user_repo.buscar_senha_por_login(login)

        if not senha_hash:
            return False

        return bcrypt.checkpw(senha.encode("utf-8"), senha_hash) 

    def _hash_senha(self, senha: str) -> bytes:
        """Gera um hash seguro para a senha"""
        if not senha or len(senha) < 6:
            raise ValueError("Senha inválida")

        senha_bytes = senha.encode("utf-8")
        return bcrypt.hashpw(senha_bytes, bcrypt.gensalt())