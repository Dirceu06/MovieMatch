from pydantic import BaseModel

class UserRequest(BaseModel):
    login: str

class SugestaoRequest(BaseModel):
    login: str
    gen: list
    adulto: bool
    brasil: bool
    anoINI: int
    anoFIM: int
    
class Login(BaseModel):
    login: str
    senha: str
    
class CadastroRequest(BaseModel):
    nome: str
    login: str
    senha: str
    adulto: bool
    
class Gostos(BaseModel):
    login: str
    gen_list: list
   
class Avaliar(BaseModel):
    filme_id: int
    filme_gen: list
    login: str
    avaliacao: bool
    
class Relacionamento(BaseModel):
    login: str
    login_amigo: str