"""
Module for a game state.
"""
from typing import List, Any
import doctest


class CurrentState:
    """
    An abstract class that defines a state in a game.

    ===Attributes===
    get_instructions: get's the instructions for the game
    str_to_move: converts a string from the user into a move for the game
    is_over: returns a bool stating whether the game is over
    is_winner: returns a bool stating if a player is a winner of a game.
    """
    def __init__(self, is_p1_turn: bool)-> None:
        """
        Initialilze the variables for the abstract game state class.
        @param player_one_turn: a boolean that expresses whether it is player
        one's turn or not.
        """
        self.player_one_turn = is_p1_turn
        self.get_possible_moves()
        self.get_current_player_name()

    def __str__(self) -> str:
        """Return a string representation of the current state of the game.
        """
        return "{} is the current player \nThe possible moves available are " \
               "{}.".format(self.get_current_player_name(),
                            str(self.get_possible_moves()))

    def __eq__(self, other) -> bool:
        """Return whether current state self is equal to anoter current state.
        """
        return (self.player_one_turn == other.player_on_turn) and \
               (self.get_possible_moves() == other.get_possible_moves()) and \
               (self.get_current_player_name() ==
                other.get_current_player_name())

    def is_valid_move(self, move_to_make: object) -> bool:
        """Return whether a specific move is valid to play on the game.
        """
        if move_to_make in self.get_possible_moves():
            return True
        else:
            return False

    def get_current_player_name(self) -> str:
        """Return a string representation of the current player
        """
        if self.player_one_turn:
            return "p1"
        else:
            return "p2"

    def get_possible_moves(self) -> List[Any]:
        """Return a list of the possible moves in the game given a
        current state.
        """
        raise NotImplementedError("Subclass must implement!")

    def make_move(self, move_to_make: object) -> object:
        """apply a specific move to a game state in order to initialize a new
        game state.
        """
        raise NotImplementedError("Subclass must implement!")
