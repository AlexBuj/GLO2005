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
    db=app.config['MYSQL_DB'],
    autocommit=True
)


def get_stock_info(symbol):
    '''
    Fonction qui récupère les données sur l'API. KEY: 2c60e6e984a34692611edd82e4b4f308
    '''
    api_key = '2c60e6e984a34692611edd82e4b4f308'
    url = f'https://financialmodelingprep.com/api/v3/quote-short/{symbol}?apikey={api_key}'

    response = requests.get(url)
    if response.status_code == 200:
        stock_data = response.json()
        if stock_data:
            return stock_data[0]  # Retourne les données du titre
        else:
            return None
    else:
        print("Erreur lors de la requête API:", response.status_code)
        return None


def get_company_info(symbol):
    '''
    Fonction qui récupère les données sur l'API. KEY: 2c60e6e984a34692611edd82e4b4f308
    '''
    api_key = '2c60e6e984a34692611edd82e4b4f308'
    url = f'https://financialmodelingprep.com/api/v3/profile/{symbol}?apikey={api_key}'

    response = requests.get(url)
    if response.status_code == 200:
        company_data = response.json()
        if company_data:
            return company_data[0]  # Retourne les données de l'entreprise trouvée
        else:
            return None
    else:
        print("Erreur lors de la requête API:", response.status_code)
        return None


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
    symbole = get_stock_info('GOOG')
    cie = get_company_info('GOOG')
    return render_template("main.html", result=result, symbole=symbole, cie=cie)


if __name__ == '__main__':
    app.run(debug=True)
