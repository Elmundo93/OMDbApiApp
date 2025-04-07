import os
import random
import statistics
import requests
from dotenv import load_dotenv

# Load environment variables from .env file.
load_dotenv()

class MovieApp:
    def __init__(self, storage):
        """
        Initialize the MovieApp with a storage that implements IStorage.
        """
        self._storage = storage
        # Get the API key from environment variables.
        self.api_key = os.environ.get("OMDB_API_KEY")
        if not self.api_key:
            raise ValueError("OMDB_API_KEY not found in environment variables. Please create a .env file with your API key.")
        # Set file paths for the template and the generated website.
        self.template_file = "_static/index_template.html"
        self.website_file = "index_template.html"

    def _command_list_movies(self):
        movies = self._storage.list_movies()
        print("\nListing movies:")
        if not movies:
            print("No movies found!")
        else:
            for title, info in movies.items():
                print(f"{title} ({info['year']}), rating: {info['rating']}")
        input("\nPress enter to continue")

    def _command_add_movie(self):
        print("\nAdd movie:")
        title = input("Enter movie title: ").strip()
        # Fetch data from the OMDb API.
        try:
            url = f"http://www.omdbapi.com/?i=tt3896198&apikey={self.api_key}&t={title}"
            response = requests.get(url)
            data = response.json()
            if data.get("Response") == "False":
                print(f"Error: {data.get('Error', 'Movie not found')}")
                input("Press enter to continue")
                return
            # Extract required information.
            movie_title = data.get("Title", title)
            movie_year = int(data.get("Year", "0").split("–")[0])
            movie_rating = float(data.get("imdbRating", 0))
            movie_poster = data.get("Poster", "")
            self._storage.add_movie(movie_title, movie_year, movie_rating, movie_poster)
            print(f"Movie '{movie_title}' added successfully!")
        except Exception as e:
            print(f"An error occurred: {e}")
        input("Press enter to continue")

    def _command_delete_movie(self):
        print("\nDelete movie:")
        title = input("Enter movie title to delete: ").strip()
        try:
            self._storage.delete_movie(title)
            print(f"Movie '{title}' deleted successfully!")
        except ValueError as e:
            print(f"Error: {e}")
        input("Press enter to continue")

    def _command_update_movie(self):
        print("\nUpdate movie rating:")
        title = input("Enter movie title: ").strip()
        rating_str = input("Enter new movie rating: ").strip()
        try:
            rating = float(rating_str)
            self._storage.update_movie(title, rating)
            print(f"Movie '{title}' updated to rating {rating}")
        except ValueError as e:
            print(f"Error: {e}")
        input("Press enter to continue")

    def _command_stats(self):
        movies = self._storage.list_movies()
        print("\nMovie Stats:")
        if not movies:
            print("No movies available!")
        else:
            ratings = [info["rating"] for info in movies.values()]
            avg = statistics.mean(ratings)
            med = statistics.median(ratings)
            best_movie = max(movies.items(), key=lambda x: x[1]["rating"])
            worst_movie = min(movies.items(), key=lambda x: x[1]["rating"])
            print(f"Average rating: {avg:.2f}")
            print(f"Median rating: {med:.2f}")
            print(f"Best movie: {best_movie[0]} with rating {best_movie[1]['rating']}")
            print(f"Worst movie: {worst_movie[0]} with rating {worst_movie[1]['rating']}")
        input("Press enter to continue")

    def _command_random_movie(self):
        movies = self._storage.list_movies()
        print("\nRandom Movie:")
        if not movies:
            print("No movies available!")
        else:
            title = random.choice(list(movies.keys()))
            info = movies[title]
            print(f"{title} ({info['year']}), rating: {info['rating']}")
        input("Press enter to continue")

    def _command_search_movie(self):
        print("\nSearch movie:")
        query = input("Enter part of movie title: ").strip().lower()
        movies = self._storage.list_movies()
        found = False
        for title, info in movies.items():
            if query in title.lower():
                print(f"{title} ({info['year']}), rating: {info['rating']}")
                found = True
        if not found:
            print("No movies found!")
        input("Press enter to continue")

    def _command_sorted_by_rating(self):
        movies = self._storage.list_movies()
        print("\nMovies Sorted by Rating:")
        sorted_movies = sorted(movies.items(), key=lambda x: x[1]["rating"], reverse=True)
        for title, info in sorted_movies:
            print(f"{title} ({info['year']}): {info['rating']}")
        input("Press enter to continue")

    def _command_generate_website(self):
        movies = self._storage.list_movies()
        try:
            with open(self.template_file, "r", encoding="utf-8") as f:
                template = f.read()
            # Replace title placeholder.
            app_title = "My Movie App"
            template = template.replace("__TEMPLATE_TITLE__", app_title)
            # Build the movie grid HTML.
            grid_html = ""
            for movie_title, info in movies.items():
                grid_html += f"""<li class="movie">
    <h3>{movie_title}</h3>
    <img src="{info.get('poster', '')}" alt="{movie_title} poster">
    <p>Year: {info.get('year')}</p>
    <p>Rating: {info.get('rating')}</p>
</li>
"""
            template = template.replace("__TEMPLATE_MOVIE_GRID__", grid_html)
            with open(self.website_file, "w", encoding="utf-8") as f:
                f.write(template)
            print("Website was generated successfully.")
        except Exception as e:
            print(f"Error generating website: {e}")
        input("Press enter to continue")

    def run(self):
        while True:
            print("\n********** My Movies Database **********\n")
            print("Menu:")
            print("0. Exit")
            print("1. List movies")
            print("2. Add movie (API Fetch)")
            print("3. Delete movie")
            print("4. Update movie rating")
            print("5. Stats")
            print("6. Random movie")
            print("7. Search movie")
            print("8. Movies sorted by rating")
            print("9. Generate website")
            choice = input("Enter choice (0-9): ").strip()
            if choice == '0':
                break
            elif choice == '1':
                self._command_list_movies()
            elif choice == '2':
                self._command_add_movie()
            elif choice == '3':
                self._command_delete_movie()
            elif choice == '4':
                self._command_update_movie()
            elif choice == '5':
                self._command_stats()
            elif choice == '6':
                self._command_random_movie()
            elif choice == '7':
                self._command_search_movie()
            elif choice == '8':
                self._command_sorted_by_rating()
            elif choice == '9':
                self._command_generate_website()
            else:
                print("Invalid choice. Please try again.")
                input("Press enter to continue")