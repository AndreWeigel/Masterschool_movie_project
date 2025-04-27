import sys
from models.user import UserHandler

# Initialize the MovieLibrary
user_handler = UserHandler("sqlite:///movies.db")


def print_all_users():
    """Prints all users in the database."""
    print(user_handler)

def login():
    """Logs in a user."""
    print("Logging in:")
    username = input("Enter username: ")
    password = input("Enter password: ")

    if user_handler.verify_user(username,password):
        return username
    else:
        print("Incorrect username or password.")


def register():
    """Registers a new user."""
    print("Registering new user:")
    username = input("Enter username: ")
    password = input("Enter password: ")
    user_handler.create_user(username,password)


def exit_program():
    """Exits the program."""
    print("Bye!")
    sys.exit()


menu = {
    "1": ("Print all users", print_all_users),
    "2": ("Login", login),
    "3": ("Register", register),
    "4": ("Exit", exit_program),
}


def main():
    """Runs the main program loop, handling user input."""
    while True:
        username = None
        print("\nWelcome to the Movie Library User Menu:")
        for key, (description, _) in menu.items():
            print(f"{key}. {description}")

        choice = input("Enter your choice: ")
        action = menu.get(choice)

        if action:
            username = action[1]()
        else:
            print("Invalid choice. Please try again.")
        if username:
            return username


if __name__ == "__main__":
    main()
