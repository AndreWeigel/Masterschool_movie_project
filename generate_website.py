from models.movie import *


INPUT_HTML_FILE = "index_template.html"
#OUTPUT_HTML_FILE = "index.html"
TITLE_PLACEHOLDER = "__TEMPLATE_TITLE__"
MOVIE_PLACEHOLDER = "__TEMPLATE_MOVIE_GRID__"


def get_movie_grid(movies):
    """Generate an HTML grid from a list of movie dictionaries."""
    grid = '<ul class="movie-grid">\n'

    for movie in movies:

        grid += get_movie_card(movie)

    grid += '\n</ul>'
    return grid


def get_movie_card(movie):
    """Generate an HTML card for a single movie."""

    card = f"""
            <li class="movie-card">
                <a href="{movie['link']}" class="movie-card__link">
                    <div class="movie-card__content">
                        <img src="{movie['cover_art']}" alt="{movie['title']}" style="width:100px;">
                        <p class="movie-title">{movie['title']}</p>
                        <p class="movie-year">({movie['year']})</p>
                       
                    </div>
                </a>
            </li>
            """
    return card


def generate_html(user):
    """Generate an HTML file from the template."""
    try:

        library = MovieLibrary("sqlite:///movies.db")
        movies = library.get_movies_as_dict(username = user)

        with open(INPUT_HTML_FILE, "r") as f:
            html_template = f.read()

        html_template = html_template.replace(TITLE_PLACEHOLDER, "Movie Library")
        html_template = html_template.replace(MOVIE_PLACEHOLDER, get_movie_grid(movies))

        output_file = f"index_{user}.html"
        with open(output_file, "w") as f:
            f.write(html_template)

        print("HTML file created successfully.")

    except Exception as e:
        print("An error occurred while generating the HTML: ", e)


if __name__ == "__main__":
    # Initialize the MovieLibrary
    library = MovieLibrary("sqlite:///movies.db")
    movies = library.get_movies_as_dict(username='admin')

    print(movies)

