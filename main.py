from repositories.usuario_repository import UsuarioRepository
from repositories.genero_repository import GeneroRepository
from services.recomendacao_service import RecomendacaoService

class UserAtual:
    def __init__(self):
        self.login=''
        self.adulto=False
        self.nome=''
        self.gen=list()
    
def LoginECadastro(user_repo: UsuarioRepository):
    try:
        primeira = int(input('Escolha um opção\n1 - cadastro\n2 - login\n'))
    except:
        print('dado inválido!!!')
        return [False,'inválido']
    
    if primeira == 1:
        nome = input('qual seu nome? ').strip()
        login = input('qual seu login? ').strip()
        senha = input('qual será sua senha? ').strip()
        
        aux=True
        while aux:
            try:
                res = int(input('vê filmes para maiores?\n1 - sim\n2 - não\n'))
                aux=False
            except:
                print('coloque um inteiro')
            
        adulto=False
        
        if res==1: adulto=True
        else: adulto=False
        
        if user_repo.inserir_usuario(login,nome,senha,adulto) == False:
            print('usuario já existe, tente novamente')
        
        return [False,'inválido']
            
    else:
        login = input('qual seu login? ')
        senha = input('qual será sua senha? ')
        if user_repo.autenticar_usuario(login,senha):
            print('bem vindo')
        else:
            return [False,'none']
            
        return [True,login]

def CapturarGostos(userID, gen_repo: GeneroRepository):
    gen = gen_repo.carregar_generos_tmdb()
    
    print("agora que generos lhe agradam? ")
    for g in gen:
        print(f'ID: {g['id']} nome: {g['name']}')

    genLikes = input('Dos generos acima liste por ID quais lhe agrada: (ex: x,y,z,a,b...) ')
    genLikes=genLikes.strip().split(',')
    user_repo.associar_generos_usuario(userID,genLikes)
                 
def ExibirAvaliarFilme(userGen, userID, userAdulto, sugest_service: RecomendacaoService):
    sugestao = sugest_service.gerar_sugestoes(userGen, userID, userAdulto, limite=5)
    print('\n\nAvalie as sugestões\n')
    for s in sugestao:
        sID=s['id']
        sGenID=s['genre_ids']
        print(f'\ntitulo: {s['title']}\nmédia de nota: {s['vote_average']}\ndata de lançamento: {s['release_date']}\nResumo:\n{s['overview']}\n')
        
        repValido = False
        while not repValido:
            opn = input('gostou?\n1 - sim\n2 - não\n')
            try:
                if int(opn.strip())==1: opn=True
                else:      opn = False
                repValido = True
            except:
                print('resposta inválida')
        
        sugest_service.avaliar_filme(userID,sID,sGenID,opn)

user = UserAtual()
recomenda_service = RecomendacaoService()
genero_repo = GeneroRepository()
user_repo = UsuarioRepository()

login=False

while not login: login,user.login=LoginECadastro(user_repo)
    
user.nome,user.adulto = user_repo.buscar_info_usuario(user.login)

CapturarGostos(user.login, genero_repo)
user.gen = genero_repo.buscar_por_usuario(user.login)

ExibirAvaliarFilme(user.gen,user.login,user.adulto,recomenda_service)