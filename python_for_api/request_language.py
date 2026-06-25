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
