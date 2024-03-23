import pymysql
import os
from dotenv import load_dotenv
import requests

# Connexion à la base de données
load_dotenv()
MYSQL_HOST = os.environ.get("HOST")
MYSQL_PORT = int(os.environ.get("PORT"))
MYSQL_USER = os.environ.get("USER")
MYSQL_PASSWORD = os.environ.get("PASSWORD")
MYSQL_DB = os.environ.get("DATABASE")

connection = pymysql.connect(host=MYSQL_HOST,
                             port=MYSQL_PORT,
                             user=MYSQL_USER,
                             password=MYSQL_PASSWORD,
                             database=MYSQL_DB,
                             autocommit=True)

def read_file(path):
    file = open(path, 'r')
    return file.read().split('\n')

def set_BD_table_stocks():
    '''
    Fonction qui récupère les données sur l'API. KEY: 2c60e6e984a34692611edd82e4b4f308
    '''
    api_key = '2c60e6e984a34692611edd82e4b4f308'
    quote_url = 'https://financialmodelingprep.com/api/v3/quote/'

    list_sym = read_file("listeStocks.txt")

    # Construire une chaîne de symboles séparés par des virgules pour la requête unique
    symbols_str = ','.join(list_sym)

    # Faire une requête pour obtenir les informations sur tous les titres en une seule fois
    quote_response = requests.get(f'{quote_url}{symbols_str}?apikey={api_key}')
    if quote_response.status_code == 200:
        stocks = quote_response.json()
        cursor = connection.cursor()
        for stock in stocks:
            sym = stock['symbol']
            name = stock['name']
            prix = stock['price']
            capt = stock['marketCap']
            div = 0
            vol = stock['volume']
            fluct = stock['changesPercentage']

            cursor.execute("INSERT INTO Stocks (ticker, nom, prix, capitalisation, dividende, fluctuation, volume) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                       (sym, name, prix, capt, div, fluct, vol))


        cursor.close()
        return quote_response.json()
    else:
        print("Erreur lors de la requête API:", quote_response.status_code)
        return None


set_BD_table_stocks()

connection.close()












