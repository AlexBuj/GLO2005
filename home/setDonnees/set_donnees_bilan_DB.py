import pymysql
import os
from dotenv import load_dotenv
from datetime import datetime
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

def set_BD_bilan_cie():
    '''
    Fonction qui récupère les données sur l'API. KEY: 2c60e6e984a34692611edd82e4b4f308
    '''
    api_key = '2c60e6e984a34692611edd82e4b4f308'
    bilan_url = "https://financialmodelingprep.com/api/v3/income-statement/"

    list_sym = read_file("listeStocks.txt")
    date_actuelle = datetime.now()
    annee = date_actuelle.year
    x = 0
    for sym in list_sym:
        if x == 10:
            break
        x += 1
        # Faire une requête pour obtenir le bilan le plus récent de chaque cie.
        bilan_response = requests.get(f'{bilan_url}{sym}?period=2023&apikey={api_key}')
        if bilan_response.status_code == 200:
            bilan_list = bilan_response.json()
            bilan = [element for element in bilan_list if element['date'].startswith(str(annee-1))]
            bilan = bilan[0]
            cursor = connection.cursor()

            cik = bilan['cik']
            sym = bilan['symbol']
            cout_op = bilan['operatingExpenses']
            cout_rd = bilan['researchAndDevelopmentExpenses']
            cout_v = bilan['sellingGeneralAndAdministrativeExpenses']
            revenue = bilan['revenue']
            profit = bilan['grossProfit']

            cursor.execute("INSERT INTO Bilan (cik, ticker, coutOperation, coutRD, coutVente, revenue, profit ) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                        (cik, sym, cout_op, cout_rd, cout_v, revenue, profit))

            cursor.close()
        else:
            print("Erreur lors de la requête API:", bilan_response.status_code)
            return None
    return None

set_BD_bilan_cie()

connection.close()