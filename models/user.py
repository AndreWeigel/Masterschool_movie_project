from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
import hashlib

from models.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)

    movies = relationship("Movie", back_populates="user")

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, password):
        return self.password_hash == User.hash_password(password)

    def __str__(self):
        return f"{self.id}: {self.username}"



class UserHandler:
    def __init__(self, db_url):
        """Initializes the MovieLibrary with a database connection."""
        self.engine = create_engine(db_url)  # Creates a connection engine to database.
        Base.metadata.create_all(self.engine)  # Go through all ORM models and create the tables they define
        self.Session = sessionmaker(bind=self.engine)  # Creates a session factory

    def create_user(self, username, password):
        with self.Session() as session:
            if self.get_user_by_username(username):
                print("Username already exists")
                return None

            new_user = User(
                username=username,
                password_hash=User.hash_password(password)
            )
            session.add(new_user)
            session.commit()
            return new_user

    def get_user_by_username(self, username):
        with self.Session() as session:
            return session.query(User).filter_by(username=username).first()

    def verify_user(self, username, password):
        user = self.get_user_by_username(username)
        if user and user.verify_password(password):
            return True
        return False

    def list_users(self):
        with self.Session() as session:
            return session.query(User).all()

    def delete_user(self, username):
        user = self.get_user_by_username(username)
        if not user:
            raise ValueError("User not found")
        with self.Session() as session:
            session.delete(user)
            session.commit()

    def __str__(self):
        users = self.list_users()
        return "All users:\n" + "\n".join(str(user) for user in users)


if __name__ == "__main__":
    user_handler = UserHandler("sqlite:///movies.db")
    user_handler.create_user("admin", "admin")
    user_handler.create_user("user", "user")
    print(user_handler)


