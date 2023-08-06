"""Parity check game."""

from random import randint

import prompt

ROUNDS_NUMBER = 3


def parity_check():
    """Console game parity check."""
    name = prompt.string('May I have your name? ')
    print('Hello, {0}!'.format(name))
    print('Answer "yes" if the number is even, otherwise answer "no".')

    current_round = 0

    while current_round < ROUNDS_NUMBER:
        rand_num = randint(0, 100)
        correct_answer = 'yes' if rand_num % 2 == 0 else 'no'

        answer = prompt.string('Question: {0} \nYour answer: '.format(rand_num))

        if answer == correct_answer:
            print('Correct!')
            current_round += 1
        else:
            print('"{0}" is wrong answer ;(. Correct answer was "{1}".'.format(
                answer,
                correct_answer,
            ))
            print('Lets try again, {0}!'.format(name))
            break

        if current_round == ROUNDS_NUMBER:
            print('Congratulations, {0}!'.format(name))
