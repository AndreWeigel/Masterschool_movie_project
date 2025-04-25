# Standard library import
import sys
import statistics
import random


# Third-party imports
import matplotlib.pyplot as plt
from fuzzywuzzy import process

# Local module import
from library import MovieLibrary
import generate_website
from api_connection import search_movies_api


# Initialize the MovieLibrary
library = MovieLibrary("sqlite:///movies.db")




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
        movie_data = search_movies_api()
        if not movie_data:
            break
        title = movie_data["Title"]
        year = movie_data["Year"]
        director = movie_data["Director"]
        poster = movie_data["Poster"]
        try:
            rating = movie_data.get("Ratings", [])[0]["Value"].split('/')[0]
        except Exception:
            rating = "0"
            print(f"Rating not found for '{title}', defaulting to 0.")

        library.add_movie(title, int(year), rating, director = director, cover_art = poster)
        print(f"Movie '{title}' added successfully.")
        break


def delete_movie():
    """Deletes a movie from the dictionary if it exists."""
    title = input("\nEnter movie name to delete: ")
    library.remove_movie(title)



def update_movie():
    """Updates the rating of an existing movie."""
    title = input("\nEnter movie to update: ")

    kwargs = {}

    rating_input = input("Enter rating (0-10) or press Enter to skip this field: ")
    if rating_input:
        try:
            rating = float(rating_input)
            if 0 <= rating <= 10:
                kwargs['rating'] = rating
            else:
                print("Rating must be between 0 and 10.")
                return
        except ValueError:
            print("Invalid input. Please enter a numeric rating between 0 and 10.")
            return

    year_input = input("Enter year or press Enter to skip this field: ")
    if year_input:
        if year_input.isdigit() and len(year_input) == 4:
            kwargs['year'] = int(year_input)
        else:
            print("Invalid year. Please enter a valid 4-digit year.")
            return

    if kwargs:
        library.update_movie(title, **kwargs)
        print(f"Movie '{title}' updated successfully.")
    else:
        print("No updates provided.")


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
      11. Generate website

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
    "10": filter_movies,
    "11": generate_website.generate_html,
}


def run_menu():
    """Runs the main program loop, handling user input."""
    while True:
        choice = input(get_menu()).strip()
        action = menu_actions.get(choice)
        if action:
            action()
        else:
            print("Invalid choice! Please enter a number from 0-10.")


if __name__ == "__main__":
    run_menu()
