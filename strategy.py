from typing import Any
from game import CurrentState
from substract_square import SubstractSquare
from chopsticks import Chopsticks
import random

# TODO: Adjust the type annotation as needed.


def interactive_strategy(game: Any) -> Any:
    """
    Return a move for game through interactively asking the user for input.
    """

    move = input("Enter a move: ")
    return game.str_to_move(move)

# TODO: Implement a random strategy.


def random_strategy(game: Any) -> Any:
    """
    Return a move for game through a randomly computer generated list of moves.
    """

    chosen_move = random.choice(game.current_state.get_possible_moves())
    return chosen_move
