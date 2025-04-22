from movie import *


class MovieLibrary:
    """Manages a collection of movies using a SQLAlchemy ORM with a SQLite database."""
    def __init__(self, db_url):
        """Initializes the MovieLibrary with a database connection."""
        self.engine = create_engine(db_url) #Creates a connection engine to database.
        Base.metadata.create_all(self.engine) #Go through all ORM models and create the tables they define
        self.Session = sessionmaker(bind=self.engine) #Creates a session factory

    def add_movie(self, title, year, rating, director=None, cover_art=None):
        """Adds a new movie to the library if it doesn't already exist."""
        with self.Session() as session:
            exists = session.query(Movie).filter_by(title=title, year=year).first()
            if exists:
                print(f"Movie '{title}' ({year}) already exists in the library.")
                return

            movie = Movie(
                title=title,
                year=year,
                rating=rating,
                director=director or "Unknown",
                cover_art=cover_art or "Missing"
            )
            session.add(movie)
            session.commit()

    def update_movie(self, title, **kwargs):
        """Updates details of an existing movie by title."""
        with self.Session() as session:
            movie = session.query(Movie).filter_by(title=title).first()
            if movie:
                if 'year' in kwargs:
                    movie.year = kwargs['year']
                if 'rating' in kwargs:
                    movie.rating = kwargs['rating']
                if 'director' in kwargs:
                    movie.director = kwargs['director']
                if 'cover_art' in kwargs:
                    movie.cover_art = kwargs['cover_art']
                session.commit()
            else:
                print(f"No movie found with title '{title}'")


    def remove_movie(self, title):
        """Removes a movie from the library by title."""
        with self.Session() as session:
            movie = session.query(Movie).filter_by(title=title).first()
            if movie:
                session.delete(movie)
                session.commit()

    def get_movies_as_movie_obj(self):
        """Returns a list of all movies in the library."""
        with self.Session() as session:
            movies = session.query(Movie).all()

        return movies

    def get_movies_as_dict(self):
        """Returns all movies in the library as a list of dictionaries."""
        with self.Session() as session:
            movies = session.query(Movie).all()
        output = []
        for movie in movies:
            output.append({
                "title": movie.title,
                "year": movie.year,
                "rating": movie.rating,
                "director": movie.director,
                "cover_art": movie.cover_art
            })
        return output


    def __str__(self):
        movies = []
        for movie in self.list_movies():
            movies.append(str(movie))
        return "\n".join(movies)



if __name__ == "__main__":
    database = 'sqlite:///movies.db'
    library = MovieLibrary(database)
    library.add_movie("The Matrix", 1999, 8.5)
    library.add_movie("The Dark Knight", 2008, 9.0)
    library.add_movie("Interstellar", 2014, 8.6)
    print(library)
    library.update_movie("Interstellar", director="Christopher Nolan")
    print(library)
