"""Brain_even package."""

from brain_games.games.brain_even import parity_check


def greet():
    """Greet user."""
    print('Welcome to the Brain Games!')


def main():
    """Run other functions."""
    greet()
    parity_check()


if __name__ == '__main__':
    main()
