# storage_json.py
import json
import os
from istorage import IStorage

class StorageJson(IStorage):
    def __init__(self, file_path):
        self.file_path = file_path
        # Initialize file with a default structure if it doesn't exist.
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump({"movies": {}}, f, indent=4)

    def _load_data(self):
        with open(self.file_path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {"movies": {}}
        return data

    def _save_data(self, data):
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

    def list_movies(self):
        data = self._load_data()
        return data.get("movies", {})

    def add_movie(self, title, year, rating, poster):
        data = self._load_data()
        movies = data.get("movies", {})
        if title in movies:
            raise ValueError(f"Movie '{title}' already exists!")
        movies[title] = {"year": year, "rating": rating, "poster": poster}
        data["movies"] = movies
        self._save_data(data)

    def delete_movie(self, title):
        data = self._load_data()
        movies = data.get("movies", {})
        if title not in movies:
            raise ValueError(f"Movie '{title}' not found!")
        del movies[title]
        data["movies"] = movies
        self._save_data(data)

    def update_movie(self, title, rating):
        data = self._load_data()
        movies = data.get("movies", {})
        if title not in movies:
            raise ValueError(f"Movie '{title}' not found!")
        movies[title]["rating"] = rating
        data["movies"] = movies
        self._save_data(data)