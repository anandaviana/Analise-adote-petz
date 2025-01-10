# Análise de resultados do Programa Adote Petz
![OMUMAO0](https://github.com/user-attachments/assets/3748538c-8ccd-47c0-b34d-75e3e036e18a)

 ## Tecnologias e ferramentas
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/python/python-original.svg" width="15" height="15"/> Python
   &nbsp;&nbsp;&nbsp;
   <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/pandas/pandas-original.svg" width="15" height="15"/> Pandas
   &nbsp;&nbsp;&nbsp;
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/vscode/vscode-original.svg" width="15" height="15" /> VS Code
    &nbsp;&nbsp;&nbsp;

## Introdução
Este foi o primeiro projeto de Análise de Dados que desenvolvi, com o objetivo de aplicar os conhecimentos adquiridos no curso Análise de Dados — Meus Primeiros Passos em Python, da PrograMaria. Durante o curso, trabalhamos com a base de dados da pesquisa Data Hackers, que traz informações sobre o mercado de dados, e realizamos uma análise com recortes de gênero e raça. Utilizamos Python para o tratamento dos dados e o Looker para criar um dashboard com os resultados. No projeto que apresento aqui, segui a mesma metodologia e utilizei as mesmas ferramentas, mas trabalhei com uma base de dados sobre adoções de gatos do programa Adote Petz, obtida por meio de uma API no portal da empresa.<br>


## Obtendo os dados
Para obtenção dos dados, utilizei Python e a biblioteca requests para acessar a API do portal, configurando uma requisição GET e salvando os dados em formato .json. Para organizar as informações e garantir a rastreabilidade dos arquivos, adicionei a data atual ao nome do arquivo JSON gerado. Usei a biblioteca datetime para formatar a data no formato YYYY-MM-DD. Para acompanhar a entrada e saída dos animais disponíveis na plataforma, rodei esse código semanalmente por um período de 3 meses.<br>
```python
import requests
import json
from datetime import datetime
import credentials
client_id = credentials.client_id
access_token = credentials.access_token

#Configurando a requisição
session = requests.Session()
url ='https://apis.petz.digital/adote/v1/pets?page=2&limit=300'
Petzheader = {
    "client_id":client_id,
    "access_token":access_token
}
#Obtendo os dados 
response = session.get(url,headers=Petzheader)
print(response.text)
dados = response.json()

# Obter a data atual para incluir no nome do arquivo
data_atual = datetime.now().strftime("%Y-%m-%d")
#Salvando arquivo
with open (f'dados_{data_atual}_1.json', 'w') as arquivo_json:
    json.dump(dados, arquivo_json, indent=4)
```

## Estruturando os dados
Com os arquivos .json salvos, o próximo passo foi transforma-los em um dataframe, formato mais estruturado e simples de analisar. Para isso, utilizei e biblioteca pandas para ler e organizar os arquivos .json em formato de linhas e colunas. Nessa etapa realizei também uma análise exploratória básica dos dados para verificar possíveis inconsistências na base, como informações faltantes ou formatos e unidades inadequadas, para aplicar então as transformações e tratamentos adequados. Esses arquivos foram salvos em .csv com sua data de obtenção no título para indicar a semana. Em minha análise, optei por analisar apenas dados de gatos em um primeiro momento, por não ter informações sobre como funciona o processo de adoção dos cachorros. Disponibilizo aqui o notebook dessa etapa.<br><br>
Em um segundo notebook, desenvolvi uma lógica para identificar, com base nos dados salvos em .csv no primeiro notebook, se os gatos foram adotados e em quantos dias. Para isso, utilizei a premissa de que os gatos ficam disponíveis para adoção por um período de até 4 semanas. Caso não sejam adotados nesse prazo, retornam ao abrigo de origem, conforme informado por uma funcionária de uma das lojas participantes do programa Adote Petz. Essa lógica permitiu calcular o tempo de permanência dos gatos no programa e determinar quais foram efetivamente adotados.
O código a seguir calcula e registra o tempo de permanência dos gatos com base na quantidade de vezes em que seu id único aparece nos dicionários .json coletados semanalmente, e também garante que cada gato seja adicionado apenas uma única vez à base de dados.<br><br>
Para realizar a análise, separei os dados em duas bases distintas: uma contendo todos os gatos e outra com os gatos já adotados. Para criar a base de dados geral, considerei o critério de permanência de até 4 semanas. Assim, validei os arquivos .json que poderiam ser incluídos na análise com base na diferença entre a data de coleta dos dados e a data atual. Se a data de coleta estava há pelo menos 4 semanas atrás, o arquivo era considerado válido para análise. Essa abordagem garante que os dados obtidos semanalmente possam ser utilizados para monitorar os gatinhos durante todo o período em que estão disponíveis para adoção.<br><br>
O código a seguir calcula e registra o tempo de permanência dos gatos com base na quantidade de vezes em que seu id único aparece nos dicionários .json coletados semanalmente, e também garante que cada gato seja adicionado apenas uma única vez à base de dados.<br>

```python
#Combinando os dataframes em um único (sem repetir os gatos)

todos_gatos = pd.DataFrame()  # DataFrame para armazenar dados únicos
permanência = {}  # Dicionário para rastrear a permanência de cada ID

for semana_id, df in semanas.items():
    #Verificando se cada mouraID está em todos_gatos e atualizar a permanência
    for moura_id in df['mouraID']:
        if moura_id in permanência:
            # Se já existe, incrementa a permanência
            permanência[moura_id] += 1
            #teste:
            if moura_id == 3302550:
              print(permanência[moura_id])
        else:
            # Se não existe, adiciona ao DataFrame todos_gatos
            todos_gatos = pd.concat([todos_gatos, df[df['mouraID'] == moura_id]], ignore_index=True)
            permanência[moura_id] = 0  # Inicializa a permanência como 0

#Atualizando a coluna de permanência no DataFrame todos_gatos
todos_gatos['PERMANÊNCIA'] = todos_gatos['mouraID'].map(permanência)

#Verificando os resultados
#print("Dicionário de permanência:", permanência)


#Filtrando os gatos cuja entrada seja uma data específica, para verificaçao
gatos_na_data = todos_gatos[todos_gatos['ENTRADA'] == '2024-10-19']
todos_gatos['ENTRADA'] = pd.to_datetime(todos_gatos['ENTRADA'])
```
Para realizar a análise, separei os dados em duas bases distintas: uma contendo todos os gatos e outra com os gatos já adotados. Para criar a base de dados geral, considerei o critério de permanência de até 4 semanas. Assim, validei os arquivos .json que poderiam ser incluídos na análise com base na diferença entre a data de coleta dos dados e a data atual. Se a data de coleta estava há pelo menos 4 semanas atrás, o arquivo era considerado válido para análise. Essa abordagem garante que os dados obtidos semanalmente possam ser utilizados para monitorar os gatinhos durante todo o período em que estão disponíveis para adoção.
```python
#Definindo as semanas válidas para análise de adoção: vamos trabalhar com um intervalo de 4 semanas - que é o tempo que os gatos podem ficar disponíveis na unidade Petz

# Ordenando as datas únicas e convertendo para o formato correto
datas = sorted(todos_gatos['ENTRADA'].unique())
print(datas)

# Definindo a data de corte para 4 semanas atrás
data_limite = datas[-1] - timedelta(weeks=4)

# Filtrando as datas que atendem à condição
datas_4_semanas_ou_mais = [data for data in datas if data <= data_limite]

# Convertendo as datas para strings formatadas sem o horário
lista_datas = [data.strftime('%Y-%m-%d') for data in datas_4_semanas_ou_mais]

# Exibindo a lista de datas
print(lista_datas)
```
Tomei o cuidado de remover integralmente os dados dos gatos cuja data de entrada correspondesse a da primeira semana de obtenção dos dados, pois não seria possível saber se sua real data de entrada na unidade foi naquela semana ou alguma semana anterior, prejudicando assim a consistência da análise. A partir da segunda semana, tendo a primeira semana como referência de comparação, os dados podem ser considerados válidos.<br><br>
Além disso, adicionei ao dataframe conjunto_analise a informação de faixa etária, que sintetiza as idades dos animais em grupos para facilitar a análise e compreensão dos dados, seguindo o seguinte critério: <br><br>
*Filhote:* menor que 12 meses <br>
*Junior:* de 12 a menor que 24 meses <br>
*Adulto:* a partir de 24 meses e menor que 72 meses <br>
*Senior:* a partir de 72 meses<br><br>
Na sequência, criei o segundo dataframe, com os dados dos gatos adotados. Para selecionar esses dados, segui o critério de que todos aqueles que tem permanência de até 3 semanas foram adotados. A quarta semana, como se refere à semana de retorno dos gatos à ong em caso de não adoção, foi desconsiderada.<br>

```python
#Definindo o conjunto de adotados: excluindo os gatos que "sumiram" na última semana, pois podem ter voltado à ong, e os com permanência maior que 4, pois pode haver erro de atualização

adotados = conjunto_analise.loc[conjunto_analise['PERMANÊNCIA']<=3]

adotados.info()
```

Assim, obtive os dataframes e pude realizar visualizações de dados tanto com pandas, que você pode conferir no notebook que está no repositóri. Também produzi com Looker um dashboard, disponível [aqui](https://lookerstudio.google.com/reporting/0fdd7c1a-8dfc-4ae0-aa51-6eda18128b82/page/p_gsfbbv7ymd). Para conferir o artigo com a análise completa dos dados, acesse o meu [Medium](https://medium.com/@anandadsv/an%C3%A1lise-de-resultados-do-programa-adote-petz-0d1e08bc1681).


