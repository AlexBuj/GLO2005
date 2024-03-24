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

def set_BD_table_nouvelles():
    '''
    Fonction qui récupère les données sur l'API. KEY: 2c60e6e984a34692611edd82e4b4f308
    '''
    api_key = '2c60e6e984a34692611edd82e4b4f308'
    nouvelles_url = "https://financialmodelingprep.com/api/v3/fmp/articles/"

    list_nouv = read_file("listeNouvelles.txt")

    # Construire une chaîne de symboles séparés par des virgules pour la requête unique
    nouv_str = ','.join(list_nouv)
    # Faire une requête pour obtenir les informations sur tous les titres en une seule fois
    nouvelles_response = requests.get(f'{nouvelles_url}?apikey={api_key}')
    if nouvelles_response.status_code == 200:
        nouvelles = nouvelles_response.json()
        cursor = connection.cursor()
        contenueNouv = nouvelles['content']
        for nouvelle in contenueNouv:
            titre = nouvelle['title']
            img = nouvelle['image']
            auteur = nouvelle['author']
            texte = nouvelle['content']
            date = nouvelle['date']
            cursor.execute("INSERT INTO Nouvelles (titre, auteur, image, texte, date) VALUES (%s, %s, %s, %s, %s)",
                       (titre, auteur, img,texte,date))

        cursor.close()
        return nouvelles_response.json()
    else:
        print("Erreur lors de la requête API:", nouvelles_response.status_code)
        return None


set_BD_table_nouvelles()

connection.close()

























