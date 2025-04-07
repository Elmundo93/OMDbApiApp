import json
import os

MOVIES_FILE = "movies.json"
MOVIES_FILE = os.path.join(os.path.dirname(__file__), MOVIES_FILE)


def load_db():
    with open(MOVIES_FILE, "r") as handle:
        return json.load(handle)


def save_db(movies):
    with open(MOVIES_FILE, "w") as handle:
        json.dump(movies, handle, indent=4)


def list_movies():
    return load_db()


def add_movie(title, year, rating, poster):
    movies = load_db()
    movies[title] = {
        'title': title,
        'year': year,
        'rating': rating,
        'poster': poster
    }
    save_db(movies)


def delete_movie(title):
    movies = load_db()
    del movies[title]
    save_db(movies)


def update_movie(title, notes):
    movies = load_db()
    movies[title]['notes'] = notes
    save_db(movies)
