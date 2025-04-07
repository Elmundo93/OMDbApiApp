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
        # Get the API key from environment variables
        self.api_key = os.environ.get("OMDB_API_KEY")
        if not self.api_key:
            raise ValueError("OMDB_API_KEY not found in environment variables. Please create a .env file with your API key.")
        # You can keep your template file paths as is or adjust them as needed.
        self.template_file = "_static/index_template.html"
        self.website_file = "index_template.html"

    # ... [rest of the methods remain unchanged] ...

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