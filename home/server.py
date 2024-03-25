import os
import re
from flask import Flask, request, redirect, session, jsonify, url_for
from flask import render_template
import requests
import uuid
import schedule
import time
import random
import pymysql.cursors
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()
app.config['MYSQL_HOST'] = os.environ.get("HOST")
app.config['MYSQL_PORT'] = int(os.environ.get("PORT"))
app.config['MYSQL_USER'] = os.environ.get("USER")
app.config['MYSQL_PASSWORD'] = os.environ.get("PASSWORD")
app.config['MYSQL_DB'] = os.environ.get("DATABASE")
app.secret_key = os.environ.get('SECRET_KEY')

mysql = pymysql.connect(
    host=app.config['MYSQL_HOST'],
    port=app.config['MYSQL_PORT'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    db=app.config['MYSQL_DB'],
    autocommit=True
)

def read_file(path):
    file = open(path, 'r')
    return file.read().split('\n')

def update_BD_table_stocks():
    '''
    Fonction qui récupère les données sur l'API. KEY: 2c60e6e984a34692611edd82e4b4f308
    '''
    api_key = '2c60e6e984a34692611edd82e4b4f308'
    quote_url = 'https://financialmodelingprep.com/api/v3/quote/'

    list_sym = read_file("setDonnees/listeStocks.txt")

    # Construire une chaîne de symboles séparés par des virgules pour la requête unique
    symbols_str = ','.join(list_sym)

    # Faire une requête pour obtenir les informations sur tous les titres en une seule fois
    quote_response = requests.get(f'{quote_url}{symbols_str}?apikey={api_key}')
    if quote_response.status_code == 200:
        stocks = quote_response.json()
        cursor = mysql.cursor()
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
            mysql.commit()

        cursor.close()
        return quote_response.json()
    else:
        print("Erreur lors de la requête API:", quote_response.status_code)
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


@app.route('/', methods=["GET", "POST"])
def index():
    '''
    Affiche la page d'acceuil.
    '''
    if request.method == "POST":
        username = request.form.get("log")
        password = request.form.get("password")
        findUser = 'SELECT * FROM utilisateurs WHERE courriel = %s AND mdp = %s;'
        print(username)
        print(password)
        cursor = mysql.cursor()
        cursor.execute(findUser, (username, password))
        user = cursor.fetchone()
        print(user)
        cursor.close()
        if user:
            # Stocker le nom d'utilisateur et le choix dans la session
            session['name'] = user[2]
            session['choix'] = user[5]
            return redirect("/main")
        else:
            return redirect("/inscription")

    return render_template("index.html")


@app.route("/inscription", methods=['GET', 'POST'])
def inscription():
    '''
    Affiche la page d'inscription.
    '''
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        age = request.form.get("age")
        password = request.form.get("password")
        choix = request.form.get("premium") == "true"
        emailPattern = r'^[^\.\s][\w\-\.{2,}]+@([\w-]+\.)+[\w-]{2,}$'
        passwordPattern = r'.{6,50}$'

        if not re.match(emailPattern, email):
            print("wrong email format")
        if not re.match(passwordPattern, password):
            print("wrong password format")

        cursor = mysql.cursor()
        cursor.execute("INSERT INTO utilisateurs (uid, nom, courriel, age, mdp, choix) VALUES (%s, %s, %s, %s, %s, %s)",
                       (random.randint(111111, 999999), name, email, age, password, choix))
        mysql.commit()

        cursor.close()
    return render_template("inscription.html")


@app.route('/main')
def main():
    # Récupérer le nom d'utilisateur depuis la session
    username = session.get('name')
    choix = session.get('choix')
    # Traiter le choix encodé en byte
    if choix == b'\x01':
        choix = True
    else:
        choix = False

    with mysql.cursor() as cursor:
        cursor.execute("SELECT * FROM Stocks")
        stocks = cursor.fetchall()
    with mysql.cursor() as cursor:
        cursor.execute("SELECT * FROM Compagnie")
        cie = cursor.fetchall()
    with mysql.cursor() as cursor:
        cursor.execute("SELECT titre, auteur, image, texte, date FROM Nouvelles")
        nouvelles = cursor.fetchall()
    return render_template("main.html", stocks=stocks, cie=cie, username=username, choix=choix, nouvelles=nouvelles)


@app.route('/info')
def info():
    sym = request.args.get('symbole')
    with mysql.cursor() as cursor:
        # Exécuter la requête SQL
        sql = "SELECT * FROM Compagnie WHERE ticker = %s"
        cursor.execute(sql, (sym,))
        result_cie = cursor.fetchall()

    with mysql.cursor() as cursor:
        # Exécuter la requête SQL
        sql = "SELECT * FROM Bilan WHERE ticker = %s"
        cursor.execute(sql, (sym,))
        result_bilan = cursor.fetchall()

    data = {
        'cie': result_cie,
        'bilan': result_bilan
    }
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
    schedule.every(24).hours.do(update_BD_table_stocks)
    while True:
        schedule.run_pending()
        time.sleep(1)
