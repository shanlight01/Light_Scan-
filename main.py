# Importation de la classe principale de l'application depuis le module ui.app
from ui.app import App
from database.db_connection import init_db

# Point d'entrée du programme
# Cette condition vérifie si le script est exécuté directement (et non importé)
if __name__ == "__main__":
    # Initialisation de la connexion à la base de données MySQL
    # Cela créera les tables si elles n'existent pas encore
    init_db()
    
    # Instanciation de l'application
    app = App()
    # Démarrage de la boucle principale de l'interface graphique (GUI)
    # Cela permet à l'application de rester ouverte et de réagir aux actions de l'utilisateur
    app.mainloop()
