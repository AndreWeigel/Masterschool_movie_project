from sqlalchemy import Column, Integer, String, Float, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


from models.base import Base
from models.user import User


class Movie(Base):
    """Represents a movie in the database."""
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    rating = Column(Float, nullable=False)
    director = Column(String, default="Unknown")
    cover_art = Column(String, default="Missing")
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="movies")

    def __str__(self):
        return f"{self.title} ({self.year}), directed by {self.director}"


class MovieLibrary:
    """Manages a collection of movies using a SQLAlchemy ORM with a SQLite database."""
    def __init__(self, db_url,):
        """Initializes the MovieLibrary with a database connection."""
        self.engine = create_engine(db_url) #Creates a connection engine to database.
        Base.metadata.create_all(self.engine) #Go through all ORM models and create the tables they define
        self.Session = sessionmaker(bind=self.engine) #Creates a session factory

    def add_movie(self, title, year, rating, director=None, cover_art=None, username=None):
        """Adds a new movie to the library if it doesn't already exist."""
        with self.Session() as session:
            if username:
                user = session.query(User).filter_by(username=username).first()
                if not user:
                    user = User(username=username)
                    session.add(user)
                    session.commit()
            exists = session.query(Movie).filter_by(title=title, year=year, user_id=user.id).first()
            if exists:
                print(f"Movie '{title}' ({year}) already exists in the library for user '{username}'.")
                return

        movie = Movie(
                title=title,
                year=year,
                rating=rating,
                director=director or "Unknown",
                cover_art=cover_art or "Missing",
                user_id = user.id
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
                print(f"Movie '{title}' removed from the library.")
            else:
                print(f"No movie found with title '{title}'")

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

