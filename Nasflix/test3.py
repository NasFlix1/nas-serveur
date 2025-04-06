import sqlite3

# Fonction pour se connecter à la base de données
def connect_db():
    db_path = '/home/theo/Nasflix/base de données/base_de_données.db'  # Remplace par ton chemin
    conn = sqlite3.connect(db_path)
    return conn

# Fonction pour récupérer et afficher les colonnes d'une table
def get_column_names(table_name):
    conn = connect_db()  # Connexion à la base de données
    cursor = conn.cursor()
    
    # Exécute la commande PRAGMA pour obtenir les informations sur les colonnes
    cursor.execute(f'PRAGMA table_info({table_name})')
    
    # Récupérer les informations des colonnes
    columns = cursor.fetchall()
    
    # Afficher les noms des colonnes
    print(f"Noms des colonnes dans la table '{table_name}':")
    for column in columns:
        print(f"- {column[1]}")  # Le nom de la colonne est à l'index 1
    
    conn.close()

# Nom de la table à analyser
table_name = 'films'  # Remplace par le nom de ta table

# Afficher les colonnes de la table
get_column_names(table_name)

