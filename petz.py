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