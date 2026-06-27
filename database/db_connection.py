import mysql.connector
from mysql.connector import Error

# Configuration de la connexion MySQL
# Pensez à modifier ces informations dans database/config.py
try:
    from database.config import DB_CONFIG
except ImportError:
    print("Erreur: Le fichier database/config.py est introuvable.")
    DB_CONFIG = {}

def get_connection():
    """
    Crée et retourne une connexion à la base de données MySQL.
    """
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            return conn
    except Error as e:
        print(f"Erreur lors de la connexion à MySQL : {e}")
        return None

def init_db():
    """
    Initialise la base de données en créant les tables nécessaires.
    Assurez-vous que la base de données 'light_scan' existe déjà dans votre MySQL,
    sinon retirez 'database' de DB_CONFIG temporairement pour la créer ici.
    """
    conn = get_connection()
    if conn is None:
        print("Impossible d'initialiser la BDD car la connexion a échoué.")
        return
        
    cursor = conn.cursor(dictionary=True) # Pour avoir les résultats sous forme de dictionnaire
    
    try:
        # Exemple : Création d'une table pour l'historique des scans
        # (La syntaxe est adaptée pour MySQL : AUTO_INCREMENT)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scans (
                id INT AUTO_INCREMENT PRIMARY KEY,
                scan_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                target VARCHAR(255) NOT NULL,
                status VARCHAR(50)
            )
        ''')
        
        # Valide les changements
        conn.commit()
        print("Tables MySQL vérifiées/initialisées avec succès.")
    except Error as e:
        print(f"Erreur lors de la création des tables : {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    # Test simple pour vérifier que la connexion fonctionne
    # Assurez-vous que votre serveur MySQL est lancé !
    init_db()
