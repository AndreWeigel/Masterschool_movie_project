# Standard library import
import sys
import statistics
import random

# Third-party imports
import matplotlib.pyplot as plt
from fuzzywuzzy import process

# Local module import
import movie_storage


def exit_menu():
    """Exits the program."""
    print("Bye!")
    sys.exit()


def list_movies():
    """Displays the list of movies along with their ratings and years."""
    movies = movie_storage.get_movies()
    # Displays the list of movies and their ratings.
    print(f"{len(movies)} movies in total")
    for movie, details in movies.items():
        print(f"{movie} - Rating: {details['rating']} - Year: {details['year']}")


def add_movie():
    """Adds a new movie to the dictionary with its rating."""
    movies = movie_storage.get_movies()
    while True:
        title = input("\nEnter movie title: ")
        if not title:
            print("Movie title cannot be empty. Please enter a valid title.")
            continue
        if title in movies:
            print(f"Movie {title} already exist!")
            return

        try:
            rating = float(input("Enter rating (0-10): "))
            if rating < 0 or rating > 10:
                print("Rating must be between 0 and 10.")
                continue
        except ValueError:
            print("Invalid input. Please enter a numeric rating between 0 and 10.")
            continue

        year = input("Enter year: ")
        if not year.isdigit() or len(year) != 4:
            print("Invalid year. Please enter a valid 4-digit year.")
            continue

        movie_storage.add_movie(title, year, rating)
        print(f"Movie '{title}' added successfully.")

        break


def delete_movie():
    """Deletes a movie from the dictionary if it exists."""
    title = input("\nEnter movie name to delete: ")
    movies = movie_storage.get_movies()
    if title not in movies:
        print(f"Error: Movie '{title}' not found.")
        return
    movie_storage.delete_movie(title)
    print(f"Movie '{title}' deleted successfully.")


def update_movie():
    """Updates the rating of an existing movie."""
    movies = movie_storage.get_movies()
    title = input("\nEnter movie to update: ")
    if title in movies:
        while True:
            try:
                rating = float(input("Enter rating (0-10): "))
                if rating < 0 or rating > 10:
                    print("Rating must be between 0 and 10.")
                    continue
            except ValueError:
                print("Invalid input. Please enter a numeric rating between 0 and 10.")
                continue

            year = input("Enter year: ")
            if not year.isdigit() or len(year) != 4:
                print("Invalid year. Please enter a valid 4-digit year.")
                continue

            movie_storage.update_movie(title, year, rating)
            print(f"Movie '{title}' updated successfully.")
            break
    else:
        print(f"ERROR: Movie '{title}' not found.")


def show_stats():
    """Displays statistical analysis of movie ratings."""
    movies = movie_storage.get_movies()
    # Displays various statistics about the movie ratings.
    ratings = [details["rating"] for details in movies.values()]
    avg_rating = round(statistics.mean(ratings),1)  # Calculate average rating
    median_rating = round(statistics.median(ratings),1)  # Calculate median rating

    # Find the highest-rated movies
    highest_rating = max(ratings)
    best_movies = \
        [movie for movie, details in movies.items() if details["rating"] == highest_rating]
    best_movies = ', '.join(best_movies)

    # Find the lowest-rated movies
    lowest_rating = min(ratings)
    worst_movies = \
        [movie for movie, details in movies.items() if details["rating"] == lowest_rating]
    worst_movies = ', '.join(worst_movies)

    # Display the statistics
    print(f"""
  The average rating is: {avg_rating}
  The median rating is: {median_rating}
  Best movies (by rating): {best_movies}
  Worst movies (by rating): {worst_movies}
  """)


def random_movie():
    """Selects and displays a random movie from the database."""
    movies = movie_storage.get_movies()
    # Selects and displays a random movie from the dictionary.
    movie = random.choice(list(movies.keys()))
    print(f"Random Movie Pick: {movie}, "
          f"Rating: {movies[movie]['rating']}, Year: {movies[movie]['year']}")


def search_movie():
    """Searches for movies by a given substring or suggests similar names."""
    movies = movie_storage.get_movies()
    # Searches for movies that contain a user-inputted substring.
    part = input("\nEnter part of the movie name to search: ").lower()
    results = {}
    # Direct search
    for movie, rating in movies.items():
        if part in movie.lower():
            results[movie] = rating

    if results:
        for movie, rating in results.items():
            print(f"{movie}, {rating}")
    else:
        # Fuzzy Search
        best_match = process.extract(part, movies.keys(), limit=3)
        for match in best_match:
            print(f"{match[0]}, {movies[match[0]]}")


def sort_movies_by_rating():
    """Sorts and displays movies by their ratings in descending order."""
    movies = movie_storage.get_movies()
    # Sorts and displays movies in descending order of their ratings.
    for movie in sorted(movies, key = lambda movie: movies[movie]["rating"], reverse = True):
        print(f"{movie}, {movies[movie]['rating']}")


def create_rating_histogram():
    """Creates and saves a histogram of movie ratings."""
    movies = movie_storage.get_movies()
    # Plots a histogram of movie ratings.
    filename = input("Enter filename to save histogram: ")

    # Create histogram plot
    ratings = [details["rating"] for details in movies.values()]
    plt.hist(ratings, edgecolor='black', range=(0, 10))
    plt.xlabel("Ratings")
    plt.ylabel("Number of Movies")
    plt.title("Histogram of Movie Ratings")

    # Save plot as .png
    plt.savefig(filename + ".png")
    print(f"Histogram saved as {filename}")


def filter_movies():
    """Filters movies by minimum rating, start year, and end year."""
    movies = movie_storage.get_movies()

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
    for movie, details in movies.items():
        rating = details["rating"]
        year = int(details["year"])

        if min_rating is not None and rating < min_rating:
            continue
        if start_year is not None and year < start_year:
            continue
        if end_year is not None and year > end_year:
            continue

        filtered_movies.append((movie, year, rating))

    print("\nFiltered Movies:")
    for movie, year, rating in filtered_movies:
        print(f"{movie} ({year}): {rating}")


def get_menu():
    """Displays the main menu options."""
    start_message = """
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

      Enter choice (0-9): 
    """
    return start_message


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
        choice = input(get_menu())
        action = menu_actions.get(choice)
        if action:
            action()
        else:
            print("Invalid choice! Please enter a number from 0-9.")

if __name__ == "__main__":
    main()
