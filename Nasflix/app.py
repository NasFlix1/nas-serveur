import os
import re
from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

ROOT_DIR = "/"  # Répertoire racine

def connect_db():
    db_path = '/home/theo/Nasflix/base de données/base_de_données.db'
    return sqlite3.connect(db_path)

def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mediatheques (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           nom TEXT NOT NULL,
           categorie TEXT NOT NULL,
           chemin TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

create_table()

# 🔍 Fonction pour extraire titre, année et ID
def extract_film_info(nom_fichier):
    nom_sans_ext = os.path.splitext(nom_fichier)[0]

    # Regex : Titre (2023) [tmdbid-12345] ou [imdbid-tt7654321]
    pattern = r'^(.*?)\s*\(?(\d{4})?\)?\s*(\[.*?id-[^\]]+\])?'
    match = re.match(pattern, nom_sans_ext)

    titre = match.group(1).strip() if match and match.group(1) else nom_sans_ext
    annee = match.group(2) if match and match.group(2) else "Inconnue"
    id_tag = match.group(3) if match and match.group(3) else "ID manquant"

    return titre, annee, id_tag

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/accueil')
def accueil():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id, nom, categorie, chemin FROM mediatheques')
    mediatheques = cursor.fetchall()
    conn.close()
    return render_template('accueil.html', mediatheques=mediatheques)

@app.route('/films')
def films():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT chemin FROM mediatheques WHERE categorie = 'Films'")
    result = cursor.fetchone()
    conn.close()

    films = []
    if result:
        folder_path = result[0]
        try:
            for file in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file)
                if os.path.isfile(file_path):
                    mod_time = os.path.getmtime(file_path)
                    date_modif = datetime.fromtimestamp(mod_time).strftime("%d/%m/%Y %H:%M")

                    # 🧠 Extraire les infos du fichier
                    titre, annee, id_tag = extract_film_info(file)

                    films.append({
                        'nom': file,
                        'titre': titre,
                        'annee': annee,
                        'id': id_tag,
                        'date': date_modif
                    })
        except Exception as e:
            print(f"Erreur lors de l'accès au dossier : {e}")
    else:
        print("Aucun dossier 'films' trouvé dans la base de données.")

    return render_template('films.html', films=films)

@app.route('/films_detail/<int:id>')
def film_detail(id):
    conn = connect_db()
    cursor = conn.cursor()
    
    # Récupère les informations du film par son id
    cursor.execute("SELECT id, nom, categorie, chemin FROM mediatheques WHERE id = ?", (id,))
    film = cursor.fetchone()
    conn.close()
    
    if film:
        # Récupère les informations supplémentaires si nécessaire (comme la couverture ou autre)
        return render_template('films_detail.html', film=film)
    else:
        return "Film non trouvé", 404

@app.route('/get_folders', methods=['GET'])
def get_folders():
    dir_path = request.args.get('path', ROOT_DIR)
    folders = []
    try:
        for folder in os.listdir(dir_path):
            folder_path = os.path.join(dir_path, folder)
            if os.path.isdir(folder_path):
                folders.append(folder)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})
    return jsonify({'status': 'success', 'folders': folders, 'current_path': dir_path})

# Vérifier si le film existe déjà dans la base de données
def film_exists(titre, annee):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM films WHERE titre = ? AND date = ?", (titre, annee))
    count = cursor.fetchone()[0]
    conn.close()
    return count > 0

@app.route('/save_folder', methods=['POST'])
def save_folder():
    data = request.get_json()
    nom = data.get('nom')  # Titre du film
    chemin = data.get('path')  # Chemin du fichier du film
    
    # Extraction de l'année à partir de la date de modification du fichier
    date_modif = datetime.now()  # Utiliser la date actuelle
    annee = date_modif.year  # Extraire l'année
    
    # Générer l'ID sous la forme nom_du_film_année
    film_id = f"{nom.replace(' ', '_').lower()}_{annee}"

    # Vérifier si le film existe déjà
    if not film_exists(nom, annee):
        try:
            # Connexion à la base de données
            conn = connect_db()
            cursor = conn.cursor()

            # Insertion dans la table "films"
            cursor.execute('''
                INSERT INTO films (id, titre, date, chemin)
                VALUES (?, ?, ?, ?)
            ''', (film_id, nom, annee, chemin))

            # Validation de la transaction et fermeture de la connexion
            conn.commit()
            conn.close()

            return jsonify({'status': 'success', 'message': f"Film '{nom}' ajouté avec succès."})
        except sqlite3.Error as e:
            return jsonify({'status': 'error', 'message': f"Erreur SQLite : {str(e)}"})
    else:
        return jsonify({'status': 'error', 'message': f"Le film '{nom}' existe déjà dans la base de données."})


if __name__ == '__main__':
    app.run(debug=True)
