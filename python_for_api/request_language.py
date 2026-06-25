import os
import requests

# # Pede pro Github uma lista de eventos públicos (tipo um "feed de novidades")
# r = requests.get('https://api.github.com/events')
# print(r)

# r2 = requests.get('https://api.github.com/versions')
# print(r2)
# status = r2.status_code
# print(status)
# json = r2.json()
# print(json)

# r3 = requests.get('https://api.github.com/Amazon')

# dados_json = r3.json()
# dados_do_usuario = {
#     "name" : dados_json.get('name'),
#     "login" : dados_json.get('login'),
#     "public_repos" : dados_json.get('public_repos'),
#     "created_at" : dados_json.get('created_at')
# }

# print(dados_do_usuario)


# fazendo autenticacao com meu token ( GITHUB )
# o token é tipo uma senha secreta. NUNCA escreva ela direto no código,
# por isso ela vem de uma variável de ambiente (uma "gaveta" fora do código)
token = os.environ.get('GITHUB_TOKEN')

# headers é como um envelope que vai junto com a carta (a requisição).
# nele a gente coloca o token (pra provar quem somos) e a versão da API que queremos usar
headers = {'Authorization': 'Bearer ' + token, 'X-GitHub-Api-Version': '2022-11-28'}

api_base_url = 'https://api.github.com'
owner = 'amzn'  # definindo o usuario que vamos extrair os dados
url = f'{api_base_url}/users/{owner}/repos'
print(url)

response = requests.get(url, headers=headers)
response.status_code

# gerando as informacoes em Json da Amazon
r = response.json()
print(r)

# Verificando quantos repositorios tem na Amazon
repositorios_amazon = len(response.json())
print(repositorios_amazon)

# fazendo processo de paginacao
# a API só manda 30 resultados por vez. Pra pegar tudo, a gente vai pedindo
# página 1, página 2, página 3... até a API responder uma página vazia,
# que é o sinal de "acabou, não tem mais nada"
repost_list = []  # lista vazia que vai guardar os repositórios de todas as páginas
page_num = 1

while True:
    try:
        url_page = f'{url}?page={page_num}'
        response = requests.get(url_page, headers=headers)
        page_data = response.json()

        if len(page_data) == 0:  # página vazia = não tem mais repositórios
            break

        repost_list.extend(page_data)
        page_num += 1
    except Exception:  # se algo der errado na requisição, paramos o loop
        break

paginacao_repositorios_amazon = len(repost_list)
print(paginacao_repositorios_amazon)


# ===================== ANOTAÇÕES (NOTES) =====================
# Resuminho simples de cada coisa, pra explicar pra alguém que tá começando agora:

# GET -> é como "pedir pra ver" uma informação. Não muda nada, só consulta.

# requests.get(url, ...) -> é o comando em Python que faz esse "pedido" pra API.

# params -> filtros que a gente manda junto na URL, tipo "me mostra só ordenado por nome".

# headers -> é o envelope da carta. Vai junto com o pedido e carrega informações
#            extras, como o token de quem está pedindo.

# auth -> outra forma de mandar usuário e senha direto na requisição.

# timeout -> quanto tempo a gente espera por uma resposta antes de desistir.

# verify -> se a gente quer checar se o "site é confiável" (certificado SSL) antes de confiar nele.

# Authorization (dentro do headers) -> é onde a gente coloca o token, tipo um crachá
#            que prova "sou eu mesmo, pode me deixar entrar".

# Tipos de autenticação:
#  - API Key: uma chavinha única que identifica você. Simples, tipo senha fixa.
#  - Token: você faz login uma vez, recebe um "crachá temporário" (token) e usa ele
#           depois, sem precisar digitar a senha de novo. Pode expirar.
#  - OAuth: você nunca dá sua senha pro app de terceiro. Você loga direto no site oficial
#           (ex: Github) e só autoriza o app a usar uma parte das suas coisas.

# Paginação -> quando tem muita informação, a API divide em "páginas" (tipo um livro).
#              Por isso usamos um loop pra ir virando as páginas até não ter mais nada.

# while True + break -> "continue repetindo pra sempre, até eu mandar parar".
#              Usamos isso porque não sabíamos de antemão quantas páginas existiam.

# try / except -> "tenta fazer isso, e se der erro, faz aquilo outro" em vez de
#              o programa quebrar e parar tudo.

# O que aprendi nessa aula:
#  - Extrair dados de uma API
#  - Gerar o token de autenticação no Github
#  - Realizar requisições autenticadas
#  - Utilizar a técnica de paginação
#  - Aplicar tratamento de erros ao fazer requisições
