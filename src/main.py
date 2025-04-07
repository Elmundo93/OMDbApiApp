from storage_json import StorageJson
from movie_app import MovieApp

def main():
    # Updated file path to point to the data directory.
    storage = StorageJson("data/movies_data.json")
    app = MovieApp(storage)
    app.run()

if __name__ == "__main__":
    main()