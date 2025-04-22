# Standard library import
import sys
import statistics
import random
import os
import requests
from dotenv import load_dotenv

# Third-party imports
import matplotlib.pyplot as plt
from fuzzywuzzy import process

# Local module import
from library import MovieLibrary

# Initialize the MovieLibrary
library = MovieLibrary("sqlite:///movies.db")

import os
import requests
from dotenv import load_dotenv


def search_movies():
    load_dotenv()  # Load API key from .env file
    api_key = os.getenv("OMDB_API_KEY")

    if not api_key:
        raise ValueError("OMDB_API_KEY not found in .env file")

    search_query = input("What movie do you want to add: ").strip()
    if not search_query:
        print("Insert a valid query.")
        return None

    url = f"https://www.omdbapi.com/?s={search_query}&apikey={api_key}"
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
                return movies[choice - 1]
            else:
                print("Invalid selection. Try again.")
        except ValueError:
            print("Please enter a valid number.")


def exit_menu():
    """Exits the program."""
    print("Bye!")
    sys.exit()


def list_movies():
    """Displays the list of movies along with their ratings and years."""
    movies = library.get_movies_as_dict()
    print(f"{len(movies)} movies in total")
    for movie in movies:
        print(f"{movie['title']} - Rating: {movie['rating']} - Year: {movie['year']}")


def add_movie():
    """Adds a new movie to the dictionary with its rating."""
    while True:
        movie_data = search_movies()
        title = movie_data["Title"]
        year = movie_data["Year"]
        #director = movie_data["Director"]
        poster = movie_data["Poster"]
        while True:
            try:
                rating = float(input("Enter rating (0-10): "))
                if rating < 0 or rating > 10:
                    print("Rating must be between 0 and 10.")
                break
            except ValueError:
                print("Invalid input. Please enter a numeric rating between 0 and 10.")
                continue

        library.add_movie(title, int(year), rating, cover_art = poster)
        print(f"Movie '{title}' added successfully.")
        break


def delete_movie():
    """Deletes a movie from the dictionary if it exists."""
    title = input("\nEnter movie name to delete: ")
    library.remove_movie(title)
    print(f"Movie '{title}' deleted successfully.")


def update_movie():
    """Updates the rating of an existing movie."""
    title = input("\nEnter movie to update: ")
    try:
        rating = float(input("Enter rating (0-10): "))
        if rating < 0 or rating > 10:
            print("Rating must be between 0 and 10.")
            return
    except ValueError:
        print("Invalid input. Please enter a numeric rating between 0 and 10.")
        return

    year = input("Enter year: ")
    if not year.isdigit() or len(year) != 4:
        print("Invalid year. Please enter a valid 4-digit year.")
        return

    library.update_movie(title, year=int(year), rating=rating)
    print(f"Movie '{title}' updated successfully.")


def show_stats():
    """Displays statistical analysis of movie ratings."""
    movies = {m["title"]: m for m in library.get_movies_as_dict()}
    if not movies:
        print("No movies in the library.")
        return

    ratings = [details["rating"] for details in movies.values()]
    avg_rating = round(statistics.mean(ratings), 1)
    median_rating = round(statistics.median(ratings), 1)

    highest_rating = max(ratings)
    best_movies = ', '.join([m for m, d in movies.items() if d["rating"] == highest_rating])

    lowest_rating = min(ratings)
    worst_movies = ', '.join([m for m, d in movies.items() if d["rating"] == lowest_rating])

    print(f"""
  The average rating is: {avg_rating}
  The median rating is: {median_rating}
  Best movies (by rating): {best_movies}
  Worst movies (by rating): {worst_movies}
  """)


def random_movie():
    """Selects and displays a random movie from the database."""
    movies = list(library.get_movies_as_dict())
    if not movies:
        print("No movies available.")
        return

    movie = random.choice(movies)
    print(f"Random Movie Pick: {movie['title']} ({movie['year']}) - Rating: {movie['rating']}")


def search_movie():
    """Searches for movies by a given substring or suggests similar names."""
    movies = {m["title"]: m for m in library.get_movies_as_dict()}
    part = input("\nEnter part of the movie name to search: ").lower()

    results = {m: d for m, d in movies.items() if part in m.lower()}
    if results:
        for movie, details in results.items():
            print(f"{movie}, Rating: {details['rating']}, Year: {details['year']}")
    else:
        matches = process.extract(part, movies.keys(), limit=3)
        print("Did you mean:")
        for match in matches:
            title = match[0]
            print(f"{title}, Rating: {movies[title]['rating']}, Year: {movies[title]['year']}")


def sort_movies_by_rating():
    """Sorts and displays movies by their ratings in descending order."""
    movies = library.get_movies_as_dict()
    sorted_movies = sorted(movies, key=lambda m: m["rating"], reverse=True)
    for movie in sorted_movies:
        print(f"{movie['title']}, {movie['rating']}")


def create_rating_histogram():
    """Creates and saves a histogram of movie ratings."""
    movies = library.get_movies_as_dict()
    filename = input("Enter filename to save histogram: ").strip()
    ratings = [movie["rating"] for movie in movies]

    plt.hist(ratings, bins=10, edgecolor="black", range=(0, 10))
    plt.xlabel("Ratings")
    plt.ylabel("Number of Movies")
    plt.title("Histogram of Movie Ratings")
    plt.savefig(filename + ".png")
    print(f"Histogram saved as {filename}.png")


def filter_movies():
    """Filters movies by minimum rating, start year, and end year."""
    movies = library.get_movies_as_dict()

    while True:
        min_rating = input("Enter minimum rating: ")
        if min_rating:
            try:
                min_rating = float(min_rating)
                if min_rating < 0 or min_rating > 10:
                    print("Minimum rating must be between 0 and 10.")
                    continue
            except ValueError:
                print("Invalid input. Please enter a numeric rating between 0 and 10.")
                continue
        else:
            min_rating = None
        break

    while True:
        start_year = input("Enter start year: ")
        if start_year:
            if not start_year.isdigit() or len(start_year) != 4:
                print("Invalid year. Please enter a valid year.")
                continue
            start_year = int(start_year)
        else:
            start_year = None
        break

    while True:
        end_year = input("Enter end year: ")
        if end_year:
            if not end_year.isdigit() or len(end_year) != 4:
                print("Invalid year. Please enter a valid year.")
                continue
            end_year = int(end_year)
        else:
            end_year = None
        break

    filtered_movies = []
    for movie in movies:
        rating = movie["rating"]
        year = int(movie["year"])

        if min_rating is not None and rating < min_rating:
            continue
        if start_year is not None and year < start_year:
            continue
        if end_year is not None and year > end_year:
            continue

        filtered_movies.append((movie["title"], year, rating))

    print("\nFiltered Movies:")
    for title, year, rating in filtered_movies:
        print(f"{title} ({year}): {rating}")


def get_menu():
    """Displays the main menu options."""
    return """
      ********** My Movies Database **********

      Menu:
      0. Exit
      1. List movies
      2. Add movie
      3. Delete movie
      4. Update movie
      5. Stats
      6. Random movie
      7. Search movie
      8. Movies sorted by rating
      9. Create Rating Histogram
      10. Filter movies

      Enter choice (0-10): 
    """


menu_actions = {
    "0": exit_menu,
    "1": list_movies,
    "2": add_movie,
    "3": delete_movie,
    "4": update_movie,
    "5": show_stats,
    "6": random_movie,
    "7": search_movie,
    "8": sort_movies_by_rating,
    "9": create_rating_histogram,
    "10": filter_movies
}


def main():
    """Runs the main program loop, handling user input."""
    while True:
        choice = input(get_menu()).strip()
        action = menu_actions.get(choice)
        if action:
            action()
        else:
            print("Invalid choice! Please enter a number from 0-10.")


if __name__ == "__main__":
    main()
