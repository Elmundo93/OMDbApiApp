import csv
import os
from istorage import IStorage

class StorageCsv(IStorage):
    def __init__(self, file_path):
        self.file_path = file_path
        # If the CSV file does not exist, create it with a header.
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["title", "rating", "year", "poster"])

    def list_movies(self):
        movies = {}
        with open(self.file_path, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                title = row["title"]
                try:
                    rating = float(row["rating"])
                except ValueError:
                    rating = 0.0
                try:
                    year = int(row["year"])
                except ValueError:
                    year = 0
                poster = row["poster"]
                movies[title] = {"rating": rating, "year": year, "poster": poster}
        return movies

    def add_movie(self, title, year, rating, poster):
        movies = self.list_movies()
        if title in movies:
            raise ValueError(f"Movie '{title}' already exists!")
        with open(self.file_path, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([title, rating, year, poster])

    def delete_movie(self, title):
        movies = self.list_movies()
        if title not in movies:
            raise ValueError(f"Movie '{title}' not found!")
        movies.pop(title)
        with open(self.file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["title", "rating", "year", "poster"])
            for title, info in movies.items():
                writer.writerow([title, info["rating"], info["year"], info["poster"]])

    def update_movie(self, title, rating):
        movies = self.list_movies()
        if title not in movies:
            raise ValueError(f"Movie '{title}' not found!")
        movies[title]["rating"] = rating
        with open(self.file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["title", "rating", "year", "poster"])
            for title, info in movies.items():
                writer.writerow([title, info["rating"], info["year"], info["poster"]])