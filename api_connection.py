from dotenv import load_dotenv
import os
import requests
from requests.exceptions import RequestException

OMDB_BASE_URL = "https://www.omdbapi.com/"


def build_url(api_key, **params):
    """Builds the URL for the OMDb API."""
    query_string = "&".join(f"{key}={value}" for key, value in params.items())
    return f"{OMDB_BASE_URL}?{query_string}&apikey={api_key}"


def search_movies_api():
    """Searches for movies using the OMDb API."""
    load_dotenv()  # Load API key from .env file
    api_key = os.getenv("OMDB_API_KEY")

    if not api_key:
        raise ValueError("OMDB_API_KEY not found in .env file")

    search_query = input("What movie do you want to add: ").strip()
    if not search_query:
        print("Insert a valid query.")
        return None

    url = build_url(api_key, s=search_query)
    response = requests.get(url)

    if response.status_code != 200:
        print("Error fetching data from OMDb API")
        return None

    data = response.json()

    if data.get("Response") != "True":
        print("No movies found.")
        return None

    movies = data.get("Search", [])
    if not movies:
        print("No movies found.")
        input("Press Enter to continue.")
        return None

    print("\nSearch results:")
    for index, movie in enumerate(movies, start=1):
        print(f"{index}. {movie['Title']} ({movie['Year']})")

    print("0. None of these")

    while True:
        try:
            choice = int(input("\nChoose a movie by number: "))
            if choice == 0:
                return None
            elif 1 <= choice <= len(movies):
                movie_details = get_movie_details_api(movies[choice - 1]["Title"])
                return movie_details
            else:
                print("Invalid selection. Try again.")
        except ValueError:
            print("Please enter a valid number.")


def get_movie_details_api(movie_title):
    """Gets the details of a movie using the OMDb API."""
    load_dotenv()  # Load API key from .env file
    api_key = os.getenv("OMDB_API_KEY")

    if not api_key:
        raise ValueError("OMDB_API_KEY not found in .env file")

    url = build_url(api_key, t=movie_title)
    try:
        response = requests.get(url)
        response.raise_for_status()
    except RequestException as e:
        print(f"Error connecting to OMDb API: {e}")
        return None

    if response.status_code != 200:
        print("Error fetching data from OMDb API")
        return None

    data = response.json()

    return data
