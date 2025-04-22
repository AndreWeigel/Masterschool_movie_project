from sqlalchemy import Column, Integer, String, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Movie(Base):
    """Represents a movie in the database."""
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    rating = Column(Float, nullable=False)
    director = Column(String, default="Unknown")
    cover_art = Column(String, default="Missing")


    def __str__(self):
        return f"{self.title} ({self.year}), directed by {self.director}"



