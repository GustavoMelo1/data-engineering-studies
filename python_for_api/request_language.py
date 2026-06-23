import requests

# # Faz uma requisição GET na API e retorna um objeto Response
# r = requests.get('https://api.github.com/events')
# print(r)  

# r2 = requests.get('https://api.github.com/versions')
# print(r2)  
# status = r2.status_code
# print(status)
# json = r2.json()
# print(json)

r3 = requests.get('https://api.github.com/users/GustavoMelo1')

dados_json = r3.json()
dados_do_usuario = {
    "name" : dados_json.get('name'),
    "login" : dados_json.get('login'),
    "public_repos" : dados_json.get('public_repos'),
    "created_at" : dados_json.get('created_at')
}

print(dados_do_usuario)