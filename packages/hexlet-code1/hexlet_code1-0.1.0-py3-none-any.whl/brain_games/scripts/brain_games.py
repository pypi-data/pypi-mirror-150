#!/usr/bin/env python3
"""Brain-games package."""


from brain_games.cli import welcome_user


def greet():
    """Greet user."""
    print('Welcome to the Brain Games!')


def main():
    """Run other functions."""
    greet()
    welcome_user()


if __name__ == '__main__':
    main()
