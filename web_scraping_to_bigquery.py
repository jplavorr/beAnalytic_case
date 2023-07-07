import pandas as pd
from bs4 import BeautifulSoup
from google.cloud import bigquery


client = bigquery.Client(project="concise-flame-391010")

with open("request.txt", "r", encoding="utf-8", errors="ignore") as file:
    contents = file.read()


soup = BeautifulSoup(contents, 'html.parser')


# Encontre todos os blocos de informações do jogo
jogo_blocos = soup.find_all('tr', class_='app')


data = []
for jogo in jogo_blocos:
    appid = jogo.get('data-appid')
    nome = jogo.find('a', class_='b').text.strip()
    desconto = jogo.find_all('td')[3].text.strip().replace('%', '').replace('-', '')
    desconto = float(desconto) if desconto else None
    preco = jogo.find_all('td')[4].text.strip().replace('R$ ', '').replace(',', '.')
    preco = float(preco) if preco else None
    rating = jogo.find_all('td')[5].text.strip().replace('%', '')
    rating = float(rating) if rating else None
    end = jogo.find_all('td')[6].text.strip()
    started = jogo.find_all('td')[7].text.strip()
    release = jogo.find_all('td')[8].text.strip()

    # Nova linha para extrair a informação 'new historical low'
    new_historical_low = jogo.find('span', class_='highest-discount-major')
    new_historical_low = new_historical_low.text.strip() if new_historical_low else 'N/A'


    # Crie um dicionário com as informações e adicione à lista de dados
    data.append({
        'ID': appid,
        'Nome': nome,
        'Desconto': desconto,
        'Preco': preco,
        'Rating': rating,
        'End': end,
        'Started': started,
        'Release': release,
        'New_Historical_Low': new_historical_low 
    })



# Crie um DataFrame a partir da lista de dados
#df = pd.DataFrame(data)
client.insert_rows_json("steamDB.DescontoSteam", data)
#print(errors)
'''
df['Desconto (%)'] = df['Desconto (%)'].apply(lambda x: x.replace('%', '')).apply(lambda x: x.replace('-', '')).astype(float)
df['Rating (%)'] = df['Rating (%)'].apply(lambda x: x.replace('%', '')).astype(float)
df['Preço (R$)'] = df['Preço (R$)'].apply(lambda x: x.replace('R$ ', '').replace(',', '.')).astype(float)

'''