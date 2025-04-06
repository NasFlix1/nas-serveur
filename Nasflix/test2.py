import sqlite3
import os

def create_films_table():
    # Spécifie le chemin absolu de la base de données
    db_path = '/home/theo/Nasflix/base de données/base_de_données.db'  # Remplace par ton propre chemin

    try:
        # Vérifie si le dossier existe, sinon crée-le
        db_dir = os.path.dirname(db_path)
        if not os.path.exists(db_dir):
            print(f"Le dossier '{db_dir}' n'existe pas. Création du dossier...")
            os.makedirs(db_dir)

        # Connexion à la base de données (créera le fichier si ce n'est pas déjà fait)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Créer la table 'films' si elle n'existe pas déjà
        cursor.execute('''
           CREATE TABLE IF NOT EXISTS films (
               id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Identifiant unique
               titre TEXT NOT NULL,                   -- Titre du film
               date TEXT,                             -- Date de sortie du film
               description TEXT,                      -- Description du film
               acteurs TEXT,                          -- Liste des acteurs principaux
               qualite TEXT,                          -- Qualité du film (1080p, 4K, etc.)
               categorie TEXT,                        -- Catégorie du film (action, drame, etc.)
               chemin TEXT NOT NULL,                  -- Chemin du fichier ou du dossier du film
               affiche TEXT                           -- Chemin vers l'affiche du film
           )
        ''')

        conn.commit()  # Sauvegarde les changements
        print("Table 'films' créée avec succès ou déjà existante.")

    except sqlite3.OperationalError as e:
        print(f"Erreur SQLite : {e}")
    except Exception as e:
        print(f"Une erreur est survenue : {e}")
    finally:
        # Toujours fermer la connexion à la base de données
        if conn:
            conn.close()

if __name__ == '__main__':
    create_films_table()
