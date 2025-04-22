import json


MOVIES_FILE = "data.json"


def get_movies():
    """
    Returns a dictionary of dictionaries that contains the movies information in the database.
    """
    try:
        with open(MOVIES_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_movies(movies):
    """
    Saves all movies to the JSON file.
    """
    with open(MOVIES_FILE, "w") as file:
        json.dump(movies, file, indent=4)


def add_movie(title, year, rating):
    """
    Adds a movie to the movies database.
    """
    movies = get_movies()
    movies[title] = {"year": year, "rating": rating}
    save_movies(movies)


def delete_movie(title):
    """
    Deletes a movie from the movies database.
    """
    movies = get_movies()
    if title in movies:
        del movies[title]
        save_movies(movies)



def update_movie(title, year, rating):
    """
    Updates the rating of a movie in the movies database.
    """
    movies = get_movies()
    if title in movies:
        movies[title] = {"year": year, "rating": rating}
        save_movies(movies)

