import movie_lib_menu
from models import user_menu


def main():
    """ Handle Main menus, logging in and out."""
    while True:
        user = user_menu.main()
        movie_lib_menu.main(user)


if __name__ == "__main__":
    main()