import json
import pytest

from storage_json import StorageJson
from movie_app import MovieApp

# A fake response class to simulate requests responses.
class FakeResponse:
    def __init__(self, json_data):
        self._json_data = json_data

    def json(self):
        return self._json_data

# ---------------------------
# Fixtures for Storage and App
# ---------------------------
@pytest.fixture
def temp_storage_file(tmp_path):
    # Create a temporary file for the JSON storage.
    file_path = tmp_path / "movies_data.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump({"movies": {}}, f, indent=4)
    return str(file_path)

@pytest.fixture
def storage(temp_storage_file):
    return StorageJson(temp_storage_file)

@pytest.fixture
def movie_app(storage, tmp_path):
    app = MovieApp(storage)
    # Create temporary files for the HTML template and website output.
    template_file = tmp_path / "template.html"
    website_file = tmp_path / "website.html"
    # Write a basic HTML template with placeholders.
    template_file.write_text(
        "<html><head><title>__TEMPLATE_TITLE__</title></head>"
        "<body><ul>__TEMPLATE_MOVIE_GRID__</ul></body></html>",
        encoding="utf-8"
    )
    app.template_file = str(template_file)
    app.website_file = str(website_file)
    return app

# ---------------------------
# Tests for StorageJson
# ---------------------------
def test_add_movie(storage):
    storage.add_movie("Test Movie", 2000, 7.5, "http://example.com/test.jpg")
    movies = storage.list_movies()
    assert "Test Movie" in movies
    assert movies["Test Movie"]["year"] == 2000
    assert movies["Test Movie"]["rating"] == 7.5
    assert movies["Test Movie"]["poster"] == "http://example.com/test.jpg"
    with pytest.raises(ValueError):
        storage.add_movie("Test Movie", 2000, 7.5, "http://example.com/test.jpg")

def test_delete_movie(storage):
    storage.add_movie("Test Movie", 2000, 7.5, "http://example.com/test.jpg")
    storage.delete_movie("Test Movie")
    movies = storage.list_movies()
    assert "Test Movie" not in movies
    with pytest.raises(ValueError):
        storage.delete_movie("Non-Existing")

def test_update_movie(storage):
    storage.add_movie("Test Movie", 2000, 7.5, "http://example.com/test.jpg")
    storage.update_movie("Test Movie", 8.0)
    movies = storage.list_movies()
    assert movies["Test Movie"]["rating"] == 8.0
    with pytest.raises(ValueError):
        storage.update_movie("Non-Existing", 8.0)

# ---------------------------
# Tests for MovieApp Commands
# ---------------------------
def test_command_add_movie_success(movie_app, storage, monkeypatch):
    fake_api_response = {
        "Title": "Inception",
        "Year": "2010",
        "imdbRating": "8.8",
        "Poster": "https://example.com/inception.jpg",
        "Response": "True"
    }
    def fake_get(url):
        return FakeResponse(fake_api_response)
    monkeypatch.setattr("movie_app.requests.get", fake_get)
    inputs = iter(["Inception", ""])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))
    movie_app._command_add_movie()
    movies = storage.list_movies()
    assert "Inception" in movies
    assert movies["Inception"]["year"] == 2010
    assert movies["Inception"]["rating"] == 8.8
    assert movies["Inception"]["poster"] == "https://example.com/inception.jpg"

def test_command_add_movie_failure(movie_app, storage, monkeypatch):
    fake_api_response = {
        "Response": "False",
        "Error": "Movie not found!"
    }
    def fake_get(url):
        return FakeResponse(fake_api_response)
    monkeypatch.setattr("movie_app.requests.get", fake_get)
    inputs = iter(["Nonexistent", ""])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))
    movie_app._command_add_movie()
    movies = storage.list_movies()
    assert "Nonexistent" not in movies

def test_command_delete_movie(movie_app, storage, monkeypatch):
    storage.add_movie("Test Movie", 2000, 7.5, "http://example.com/test.jpg")
    inputs = iter(["Test Movie", ""])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))
    movie_app._command_delete_movie()
    movies = storage.list_movies()
    assert "Test Movie" not in movies

def test_command_update_movie(movie_app, storage, monkeypatch):
    storage.add_movie("Test Movie", 2000, 7.5, "http://example.com/test.jpg")
    inputs = iter(["Test Movie", "8.5", ""])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))
    movie_app._command_update_movie()
    movies = storage.list_movies()
    assert movies["Test Movie"]["rating"] == 8.5

def test_command_search_movie(movie_app, storage, monkeypatch, capsys):
    storage.add_movie("Test Movie", 2000, 7.5, "http://example.com/test.jpg")
    inputs = iter(["Test", ""])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))
    movie_app._command_search_movie()
    captured = capsys.readouterr().out
    assert "Test Movie" in captured

def test_command_list_movies_empty(movie_app, monkeypatch, capsys):
    inputs = iter([""])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))
    movie_app._command_list_movies()
    captured = capsys.readouterr().out
    assert "No movies found" in captured

def test_command_random_movie_empty(movie_app, monkeypatch, capsys):
    inputs = iter([""])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))
    movie_app._command_random_movie()
    captured = capsys.readouterr().out
    assert "No movies available" in captured

def test_command_random_movie(movie_app, storage, monkeypatch, capsys):
    storage.add_movie("Test Movie", 2000, 7.5, "http://example.com/test.jpg")
    inputs = iter([""])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))
    movie_app._command_random_movie()
    captured = capsys.readouterr().out
    assert "Test Movie" in captured

def test_command_sorted_by_rating_empty(movie_app, monkeypatch, capsys):
    inputs = iter([""])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))
    movie_app._command_sorted_by_rating()
    captured = capsys.readouterr().out
    assert "Movies Sorted by Rating:" in captured

def test_command_sorted_by_rating(movie_app, storage, monkeypatch, capsys):
    storage.add_movie("Movie A", 2000, 7.0, "http://example.com/a.jpg")
    storage.add_movie("Movie B", 2001, 8.0, "http://example.com/b.jpg")
    inputs = iter([""])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))
    movie_app._command_sorted_by_rating()
    captured = capsys.readouterr().out
    assert captured.find("Movie B") < captured.find("Movie A")

def test_command_stats_empty(movie_app, monkeypatch, capsys):
    inputs = iter([""])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))
    movie_app._command_stats()
    captured = capsys.readouterr().out
    assert "No movies available" in captured

def test_command_stats(movie_app, storage, monkeypatch, capsys):
    storage.add_movie("Movie A", 2000, 7.0, "http://example.com/a.jpg")
    storage.add_movie("Movie B", 2001, 9.0, "http://example.com/b.jpg")
    inputs = iter([""])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))
    movie_app._command_stats()
    captured = capsys.readouterr().out
    assert "Average rating:" in captured
    assert "Median rating:" in captured
    assert "Best movie:" in captured
    assert "Worst movie:" in captured

def test_command_generate_website(movie_app, storage, monkeypatch):
    storage.add_movie("Test Movie", 2000, 7.5, "http://example.com/test.jpg")
    inputs = iter([""])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))
    movie_app._command_generate_website()
    with open(movie_app.website_file, "r", encoding="utf-8") as f:
        content = f.read()
    assert "__TEMPLATE_TITLE__" not in content
    assert "__TEMPLATE_MOVIE_GRID__" not in content
    assert "Test Movie" in content