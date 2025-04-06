import sqlite3

# Connexion à la base de données
conn = sqlite3.connect('/home/theo/Nasflix/base de données/base_de_données.db')
cursor = conn.cursor()

# Exécuter la requête pour récupérer toutes les lignes de la table "films"
cursor.execute("SELECT id, titre, date, description, acteurs, qualite, categorie, chemin, affiche FROM films")
rows = cursor.fetchall()

# Affichage des informations
print("Films enregistrés :")
for row in rows:
    id_film = row[0]  # ID du film
    titre = row[1]  # Titre du film
    date = row[2]  # Date de sortie
    description = row[3]  # Description
    acteurs = row[4]  # Acteurs
    qualite = row[5]  # Qualité
    categorie = row[6]  # Catégorie
    chemin = row[7]  # Chemin du fichier
    affiche = row[8]  # Affiche du film

    print(f"ID: {id_film}, Titre: {titre}, Date: {date}, Description: {description}, "
          f"Acteurs: {acteurs}, Qualité: {qualite}, Catégorie: {categorie}, "
          f"Chemin: {chemin}, Affiche: {affiche}")

# Fermeture de la connexion à la base de données
conn.close()
