from database.db_connection import get_connection

def insert_scan(target, status="Terminé"):
    """
    Insère un nouveau scan dans la base de données MySQL.
    Retourne True si l'insertion a réussi, False sinon.
    """
    conn = get_connection()
    if conn is None:
        print("Erreur : Impossible de se connecter à la BDD pour sauvegarder le scan.")
        return False
        
    try:
        cursor = conn.cursor()
        query = "INSERT INTO scans (target, status) VALUES (%s, %s)"
        cursor.execute(query, (target, status))
        
        conn.commit()
        print(f"Scan de {target} sauvegardé en base de données.")
        return True
    except Exception as e:
        print(f"Erreur lors de l'insertion du scan : {e}")
        return False
    finally:
        if 'cursor' in locals():
            cursor.close()
        conn.close()

def get_all_scans():
    """
    Récupère tout l'historique des scans depuis la base de données.
    Retourne une liste de dictionnaires.
    """
    conn = get_connection()
    if conn is None:
        return []
        
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM scans ORDER BY scan_date DESC")
        return cursor.fetchall()
    except Exception as e:
        print(f"Erreur lors de la récupération des scans : {e}")
        return []
    finally:
        if 'cursor' in locals():
            cursor.close()
        conn.close()
