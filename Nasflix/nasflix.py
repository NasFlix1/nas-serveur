from flask import Flask, jsonify
import sqlite3
import requests
import os
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DB_PATH = "/home/theo/Nasflix/base de données/base_de_données.db"
API_KEY = "80b4210ceca9fe62fd9c53208b21e1d1"
MOVIE_DIR = "/home/theo/Téléchargements/téléchargement films/nas/films"
TV_DIR = "/home/theo/Téléchargements/téléchargement films/nas/series"

POSTER_DIR = "/home/theo/Nasflix/base de données/posters"
BACKGROUND_DIR = "/home/theo/Nasflix/base de données/backgrounds"

os.makedirs(POSTER_DIR, exist_ok=True)
os.makedirs(BACKGROUND_DIR, exist_ok=True)


def download_image(url, folder, filename):
    """Télécharge une image depuis une URL dans un dossier spécifique"""
    if not url:
        return None
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            ext = os.path.splitext(url)[1]
            local_path = os.path.join(folder, f"{filename}{ext}")
            with open(local_path, 'wb') as out_file:
                out_file.write(response.content)
            return local_path
    except Exception as e:
        print(f"Erreur téléchargement image {url} : {e}")
    return None


def get_tmdb_movie_data(movie_name):
    """ Recherche un film sur TMDb et télécharge les images """
    url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&language=fr-FR&query={movie_name}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data["results"]:
            movie = data["results"][0]
            poster_url = f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie.get("poster_path") else None
            bg_url = f"https://image.tmdb.org/t/p/w1280{movie['backdrop_path']}" if movie.get("backdrop_path") else None
            poster_path = download_image(poster_url, POSTER_DIR, movie_name)
            bg_path = download_image(bg_url, BACKGROUND_DIR, movie_name)
            return {
                "title": movie["title"],
                "year": movie["release_date"].split("-")[0] if movie["release_date"] else "N/A",
                "description": movie["overview"],
                "poster": poster_path,
                "background": bg_path
            }
    return None


def get_tmdb_tv_data(tv_name):
    """ Recherche une série sur TMDb et télécharge les images """
    url = f"https://api.themoviedb.org/3/search/tv?api_key={API_KEY}&language=fr-FR&query={tv_name}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data["results"]:
            tv = data["results"][0]
            poster_url = f"https://image.tmdb.org/t/p/w500{tv['poster_path']}" if tv.get("poster_path") else None
            bg_url = f"https://image.tmdb.org/t/p/w1280{tv['backdrop_path']}" if tv.get("backdrop_path") else None
            poster_path = download_image(poster_url, POSTER_DIR, tv_name)
            bg_path = download_image(bg_url, BACKGROUND_DIR, tv_name)
            return {
                "title": tv["name"],
                "year": tv["first_air_date"].split("-")[0] if tv["first_air_date"] else "N/A",
                "description": tv["overview"],
                "poster": poster_path,
                "background": bg_path
            }
    return None


def get_movies_from_directory():
    """ Récupère les fichiers films du dossier """
    movie_files = []
    valid_extensions = (".mp4", ".mkv", ".avi", ".mov")
    for file in os.listdir(MOVIE_DIR):
        if file.endswith(valid_extensions):
            movie_name = os.path.splitext(file)[0]
            file_path = os.path.join(MOVIE_DIR, file)
            file_date = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime("%Y-%m-%d %H:%M:%S")
            movie_files.append({"name": movie_name, "date_added": file_date})
    return movie_files


def get_series_from_directory():
    """ Récupère les fichiers séries du dossier tv-sonarr """
    series_files = []
    valid_extensions = (".mp4", ".mkv", ".avi", ".mov")
    if not os.path.exists(TV_DIR):
        return []

    for file in os.listdir(TV_DIR):
        if file.endswith(valid_extensions):
            serie_name = os.path.splitext(file)[0]
            file_path = os.path.join(TV_DIR, file)
            file_date = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime("%Y-%m-%d %H:%M:%S")
            series_files.append({"name": serie_name, "date_added": file_date})
    return series_files


def search_movie_in_db(movie_name):
    """ Cherche un film dans la base de données """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM movies WHERE title LIKE ?", (f"%{movie_name}%",))
    movie = cursor.fetchone()
    conn.close()

    if movie:
        return {
            "title": movie[1],
            "year": movie[2],
            "description": movie[3],
            "poster": movie[4],
            "background": movie[5]
        }
    return get_tmdb_movie_data(movie_name)


@app.route('/movies', methods=['GET'])
def get_movies():
    """ Renvoie tous les films détectés dans le dossier """
    return jsonify(get_movies_from_directory())


@app.route('/movie/<name>', methods=['GET'])
def get_movie_info(name):
    """ Renvoie les informations d'un film spécifique """
    result = search_movie_in_db(name)
    if result:
        return jsonify(result)
    return jsonify({"error": "Film non trouvé"}), 404


@app.route('/series', methods=['GET'])
def get_series():
    """ Renvoie toutes les séries détectées dans le dossier tv-sonarr """
    return jsonify(get_series_from_directory())


@app.route('/serie/<name>', methods=['GET'])
def get_serie_info(name):
    """ Renvoie les informations d'une série spécifique depuis TMDb """
    result = get_tmdb_tv_data(name)
    if result:
        return jsonify(result)
    return jsonify({"error": "Série non trouvée"}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2000, debug=True)
