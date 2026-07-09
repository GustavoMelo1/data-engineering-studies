import os
import requests
import pandas as pd

class DadosRepositorios:

    def __init__(self, owner):
        """owner e a conta do GitHub que vou extrair os dados."""
        self.owner = owner
        self.api_base_url = 'https://api.github.com'
        self.access_token = os.environ.get('GITHUB_TOKEN')

        self.headers = {
            'X-GitHub-Api-Version': '2022-11-28'
        }

        if self.access_token is not None:
            self.headers['Authorization'] = 'Bearer ' + self.access_token

    def lista_repositorios(self):
        """percorre ate 20 paginas, suficiente pra qualquer conta que vou usar."""
        repos_list = []
        for page_num in range(1, 100):
            try:
                url = f'{self.api_base_url}/users/{self.owner}/repos?page={page_num}'
                response = requests.get(url, headers=self.headers)
                repos_list.append(response.json())
            except Exception:
                repos_list.append(None)
        return repos_list

    def nomes_repos(self, repos_list):
        """extrai so o nome de cada repositorio da lista."""
        repo_names = []
        for page in repos_list:
            for repo in page:
                try:
                    repo_names.append(repo['name'])
                except Exception:
                    pass
        return repo_names

    def nomes_linguagens(self, repos_list):
        """extrai os nomes das linguagens dos repositorios"""
        repo_languages = []
        for page in repos_list:
            for repo in page:
                try:
                    repo_languages.append(repo['language'])
                except Exception:
                    pass
        return repo_languages

    def cria_df_linguagens(self):
        """Chama os outros metodos em sequencia e monta o DataFrame final"""
        repositorios = self.lista_repositorios()
        nomes = self.nomes_repos(repositorios)
        linguagens = self.nomes_linguagens(repositorios)

        dados = pd.DataFrame()
        dados['repository_name'] = nomes
        dados['language'] = linguagens

        return dados

#"Roubando" dados dos repositorios
amazon_rep = DadosRepositorios(owner='amzn')
linguagens_mais_usadas_amzn = amazon_rep.cria_df_linguagens()
print(linguagens_mais_usadas_amzn)

netflix_rep = DadosRepositorios(owner='netflix')
linguagens_mais_usadas_netflix = netflix_rep.cria_df_linguagens()
print(linguagens_mais_usadas_netflix)

#Salvando os dados dos repositorios

os.makedirs('dados', exist_ok=True)

linguagens_mais_usadas_amzn.to_csv('dados/linguagens_amzn.csv',index=True)
linguagens_mais_usadas_netflix.to_csv('dados/linguagens_netflix.csv',index=True)