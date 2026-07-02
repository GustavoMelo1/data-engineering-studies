import os
import requests
import pandas as pd
import base64

# exploracao inicial
# r = requests.get('https://api.github.com/events')
# print(r)
# print(r.status_code)
# print(r.json())

# r3 = requests.get('https://api.github.com/Amazon')
# dados_json = r3.json()
# dados_do_usuario = {
#     "name" : dados_json.get('name'),
#     "login" : dados_json.get('login'),
#     "public_repos" : dados_json.get('public_repos'),
#     "created_at" : dados_json.get('created_at')
# }
# print(dados_do_usuario)

# token nunca direto no codigo, vem de variavel de ambiente
token = os.environ.get('GITHUB_TOKEN')
headers = {'Authorization': 'Bearer ' + token, 'X-GitHub-Api-Version': '2022-11-28'}

api_base_url = 'https://api.github.com'
owner = 'amzn'
url = f'{api_base_url}/users/{owner}/repos'

response = requests.get(url, headers=headers)
print(response.status_code)

repos_list = []
page_num = 1

# api manda 30 por vez, while True pede pagina por pagina ate vir vazia
while True:
    try:
        url_page = f'{url}?page={page_num}'
        response = requests.get(url_page, headers=headers)
        page_data = response.json()

        if len(page_data) == 0:
            break

        repos_list.extend(page_data)
        page_num += 1
    except Exception:
        break

print(f'{len(repos_list)} repositorios encontrados')

repos_name = []
for repo in repos_list:
    repos_name.append(repo["name"])

repos_language = []
for repo in repos_list:
    repos_language.append(repo["language"])

dados_amz = pd.DataFrame()
dados_amz['repository_name'] = repos_name
dados_amz['language'] = repos_language

print(dados_amz)

dados_amz.to_csv('amazon.csv')

# #Criando um repostirio com post

# api_base_url = 'https://api.github.com'
# url = f'{api_base_url}/users/repos'

# print(url)

# #Criando um dicionario

# data = {
#     'name': 'Linguagen-Utilizadas',
#     'description': 'Repositorio com as linguagens da amz',
#     'private': False
# }

# response = requests.post(url, json=data, headers=headers)
# response.status_code

# #Formatando o Arquivo para leitura com a lib "base64"
# with open('amazon.csv', 'rb')as file:
#     content = file.read()

# enconded = base64.b64encode(content)

# #Fazendo Upload dos arquivos 
# api_base_url = 'https://api.github.com'
# username = 'GustavoMelo1'
# repo = 'linguagens-utilizadas'
# path = 'amazon.csv'

# url = f'{api_base_url}/repos/{username}/{repo}/contents/{path}'
# print(url)

# #Informacoes do Upload
# data = {
#     'message': 'Adicionando a mensagem de commit',
#     'content': enconded.decode('utf-8')  # base64, nao o binario cru
# }

# #requisicao do tipo PUT
# response = requests.put(url, json=data, headers=headers)
# response.status_code