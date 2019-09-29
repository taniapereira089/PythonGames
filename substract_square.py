"""
Module for substract square game
"""
from typing import List, Any
from game import CurrentState


class SubstractSquare:
    """
    The class representing a game of substract square
    ===Attributes===
    get_instructions: get's the instructions for the game
    str_to_move: converts a string from the user into a move for the game
    is_over: returns a bool stating whether the game is over
    is_winner: returns a bool stating if a player is a winner of a game.
    """

    def __init__(self, is_p1_turn: bool) -> None:
        """Initialize a game of subtract square.
        @param player_one_turn: a boolean that expresses whether it is player
        one's turn or not.
        @param value: a positive integer value to start the substract
        square game.
        @param current_state: refers to a current state of substract
        square game.
        """

        self.player_one_turn = is_p1_turn
        self.value = int(input("Enter a positive integer to start the game: "))
        self.current_state = SubstractSquareState(self.player_one_turn,
                                                  self.value)

    def __str__(self) -> str:
        """Return a string representation of the current state of substract
        square game.
        """

        return "The current state of the game is {}".format(str(self.value))

    def __eq__(self, other) -> bool:
        """Compare a current state of substract square with another current state
        of substract square and check for equality.
        """

        return type(self.current_state) == type(other.current_state) \
            and (self.current_state == other.current_state)

    def get_instructions(self) -> str:
        """Return a string representation of the instructions of substract
        square.
        """

        return "2 players take turns subtracting numbers from a starting " \
               "number. The winner is the person who subtracts to 0."

    def str_to_move(self, move: str)->int:
        """Return the move to make given the user input of the move as a string.
        """

        return int(move)

    def is_over(self, other)->bool:
        """Return a boolean stating if the game is over.
        """

        if other.get_possible_moves() == []:
            return True
        return False

    def is_winner(self, player: str) ->bool:
        """"Return a boolean showing whether the current player is the winner
        of substract square game.
        """

        if self.is_over(self.current_state):
            return self.current_state.get_current_player_name() != player
        else:
            return False


class SubstractSquareState(CurrentState):
    """ Initialize a game state of the subtract square game.
    ===Attributes===
    get_current_player_name: return a string representing the current player
    make_move: a method that makes a move on substract square and creates a new
    game state.
    get_possible_moves: a method that returns the possible moves allowed to be
    played given a current game class.
    is_valid_move: a boolean method that checks if a move is valid.
    """

    def __init__(self, is_p1_turn: bool, value: int) -> None:
        """
        Initialilze the variables for the substract square game state class.
        @param player_one_turn: a boolean that expresses whether it is player
        one's turn or not.
        @param value: a positive integer value to start the substract
        square game.
        """

        self.player_one_turn = is_p1_turn
        self.value = value

    def __str__(self):
        """Return a string representation of the current state of the game.
        >>> s = SubstractSquareState(True, 2)
        print(s)
        "The current state of the game is 2."
        """

        return "The current state of the game is {}".format(str(self.value))

    def __eq__(self, other):
        """Return whether current state self is equal to anoter current state.
        """

        return type(self) == type(other) and self.value == other.value \
               and self.player_one_turn == other.player_one_turn

    def get_possible_moves(self) -> List[int]:
        """Return a list of integer values representing the possible moves on
        the current state of the game.
        """

        possible_moves = []
        for i in range(1, self.value + 1):
            if i ** 0.5 == int(i ** 0.5):
                possible_moves.append(i)
        return possible_moves

    def make_move(self, move_to_make: int):
        """Apply a move on the game, and create a new current state of the game.
        """

        value = self.value
        player_one_turn = self.player_one_turn
        if self.is_valid_move(move_to_make):
            value = self.value - move_to_make
            if self.player_one_turn:
                player_one_turn = False
            else:
                player_one_turn = True
        new_game_state = SubstractSquareState(player_one_turn, value)
        return new_game_state


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config="a1_pyta.txt")
