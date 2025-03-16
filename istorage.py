
from abc import ABC, abstractmethod

class IStorage(ABC):
    @abstractmethod
    def list_movies(self):
        """
        Returns a dictionary of movies.
        Example:
        {
          "Titanic": {"rating": 9, "year": 1999, "poster": "url_to_image"},
          ...
        }
        """
        pass

    @abstractmethod
    def add_movie(self, title, year, rating, poster):
        """
        Adds a movie with the given parameters.
        """
        pass

    @abstractmethod
    def delete_movie(self, title):
        """
        Deletes the movie with the given title.
        """
        pass

    @abstractmethod
    def update_movie(self, title, rating):
        """
        Updates the movie’s rating.
        """
        pass