import sqlite3

def read_table(table_name):
    # Spécifie le chemin absolu de la base de données
    db_path = '/home/theo/Nasflix/base de données/base_de_données.db'  # Remplace par ton propre chemin

    try:
        # Connexion à la base de données
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Exécuter la requête pour sélectionner toutes les données de la table
        cursor.execute(f'SELECT * FROM {table_name}')
        
        # Récupérer toutes les lignes de la table
        rows = cursor.fetchall()

        if rows:
            print(f"Contenu de la table '{table_name}':")
            for row in rows:
                print(row)
        else:
            print(f"Aucune donnée trouvée dans la table '{table_name}'.")

    except sqlite3.OperationalError as e:
        print(f"Erreur SQLite : {e}")
    except Exception as e:
        print(f"Une erreur est survenue : {e}")
    finally:
        # Toujours fermer la connexion à la base de données
        if conn:
            conn.close()

if __name__ == '__main__':
    # Demander à l'utilisateur le nom de la table à lire
    table_name = input("Entrez le nom de la table que vous voulez lire: ")
    read_table(table_name)
