import os
from flask import Flask
from flask import render_template
import requests
import pymysql.cursors
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()
app.config['MYSQL_HOST'] = os.environ.get("HOST")
app.config['MYSQL_PORT'] = int(os.environ.get("PORT"))
app.config['MYSQL_USER'] = os.environ.get("USER")
app.config['MYSQL_PASSWORD'] = os.environ.get("PASSWORD")
app.config['MYSQL_DB'] = os.environ.get("DATABASE")

mysql = pymysql.connect(
    host=app.config['MYSQL_HOST'],
    port=app.config['MYSQL_PORT'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    db=app.config['MYSQL_DB']
)


def get_api_info():
    '''
    Fonction qui récupère les données sur l'API. KEY: X58RBG8U32Y66801
    '''
    api_key = 'X58RBG8U32Y66801'
    symbols = ['IBM', 'AAPL', 'GOOGL']  # Liste des symboles à récupérer
    for symbol in symbols:
        url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}'

        try:
            r = requests.get(url, timeout=30)
            r.raise_for_status()  # Lève une exception si la demande échoue
            data = r.json()
        except requests.exceptions.RequestException as e:
            print(f"Une erreur s'est produite lors de la récupération des données pour le symbole {symbol}: {e}")

    return data


@app.route('/')
def index():
    '''
    Affiche la page d'acceuil.
    '''
    return render_template("index.html")


@app.route("/inscription")
def inscription():
    '''
    Affiche la page d'inscription.
    '''
    return render_template("inscription.html")


@app.route('/main')
def main():
    test_sql = 'SELECT * FROM utilisateurs;'
    cursor = mysql.cursor()
    cursor.execute(test_sql)
    result = cursor.fetchall()
    return render_template("main.html", result=result)


if __name__ == '__main__':
    app.run(debug=True)
