from flask import Flask
from flask import render_template
import requests


app = Flask(__name__)

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

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('index.html', name=name)


if __name__ == '__main__':
    app.run(debug=True)