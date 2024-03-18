import pymysql
from faker import Faker
import random
import hashlib
import os
from dotenv import load_dotenv


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
                             database=MYSQL_DB)

# Générateur de données fictives
fake = Faker()


# Fonction pour générer un mot de passe aléatoire
def generate_password():
    return hashlib.sha256(str(random.random()).encode()).hexdigest()[:8]


# Générer et insérer 100 clients dans la base de données
for _ in range(100):
    # Générer un identifiant unique
    id_unique = fake.pyint(min_value=111111, max_value=999999)
    while True:
        # Vérifier si l'identifiant existe déjà dans la base de données
        with connection.cursor() as cursor:
            cursor.execute("SELECT uid FROM Utilisateurs WHERE uid = %s",  (id_unique,))
            result = cursor.fetchone()
        if result:
            # Si l'identifiant existe, en générer un autre
            id_unique = fake.pyint(min_value=111111, max_value=999999)
        else:
            # Si l'identifiant est unique, sortir de la boucle
            break

    nom = fake.name()
    courriel = fake.email()
    age = random.randint(18, 90)
    mot_de_passe = generate_password()
    choix = random.randint(0, 1)

    # Créer une commande SQL pour insérer un client dans la table Utilisateurs
    sql = "INSERT INTO Utilisateurs (uid, nom, courriel, age, mdp, choix) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (id_unique, nom, courriel, age, mot_de_passe, choix)

    # Exécuter la commande SQL
    with connection.cursor() as cursor:
        cursor.execute(sql, values)
        # Commit pour sauvegarder les changements dans la base de données
        connection.commit()

# Fermer la connexion à la base de données
connection.close()
