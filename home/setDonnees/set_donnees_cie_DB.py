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

def set_BD_table_cie():
    '''
    Fonction qui récupère les données sur l'API. KEY: 2c60e6e984a34692611edd82e4b4f308
    '''
    api_key = '2c60e6e984a34692611edd82e4b4f308'
    cieProfile_url = "https://financialmodelingprep.com/api/v3/profile/"

    list_sym = read_file("listeStocks.txt")

    # Construire une chaîne de symboles séparés par des virgules pour la requête unique
    symbols_str = ','.join(list_sym)

    # Faire une requête pour obtenir les informations sur tous les titres en une seule fois
    cieProfile_response = requests.get(f'{cieProfile_url}{symbols_str}?apikey={api_key}')
    if cieProfile_response.status_code == 200:
        stocks = cieProfile_response.json()
        cursor = connection.cursor()
        for stock in stocks:
            name = stock['companyName']
            sym = stock['symbol']
            secteur = stock['sector']
            desc = stock['description']
            ws = stock['website']
            emp = stock['fullTimeEmployees']

            cursor.execute("INSERT INTO Compagnie (NomOfficiel, ticker, secteur, description, siteweb, employes) VALUES (%s, %s, %s, %s, %s, %s)",
                       (name, sym, secteur, desc, ws, emp))


        cursor.close()
        return cieProfile_response.json()
    else:
        print("Erreur lors de la requête API:", cieProfile_response.status_code)
        return None


set_BD_table_cie()

connection.close()