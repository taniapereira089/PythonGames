"""
Module for chopsticks game
"""
from typing import List, Any, Dict
from game import CurrentState


class Chopsticks:
    """The class representing a game of chopsticks.
    ===Attributes===
    get_instructions: get's the instructions for chopsticks
    str_to_move: converts a string from the user into a move for the chopsticks
    is_over: returns a bool stating whether the game is over
    is_winner: returns a bool stating if player is a winner of a game.
    """

    def __init__(self, is_p1_turn: bool) -> None:
        """Initialize the variables for the Chopsticks game.
        @param player_one_turn: a boolean that expresses whether it is player
        one's turn or not.
        @param fingers: a dictionary representing the hands of both players
        and the values heald on each hand.
        @param current_state: refers to a current state of chopsticks game.
        """

        self.player_one_turn = is_p1_turn
        self.fingers = {'p1 left hand': 1, 'p1 right hand': 1,
                        'p2 left hand': 1, 'p2 right hand': 1}
        self.current_state = ChopsticksState(self.player_one_turn, self.fingers)

    def get_instructions(self) -> str:
        """Return a string representation of the instructions for a chopsticks
        game.
        """

        return "2 players have two hands beginning with a value of 1 on each" \
               " hand. Players take turns adding values from one of their" \
               " hands to one of their opponents hands. When the value " \
               "reaches 5, then the hand becomes 'dead,' but if the value " \
               "becomes greater than 5, then the value of the hand becomes " \
               "modulo 5. The first player to get both hands in the 'dead' " \
               "state, is the loser."

    def str_to_move(self, move: str)->object:
        """Return the move made from the user during the interactive strategy.
        """

        return move

    def __str__(self) -> str:
        """Return a string representation of the players' hands and the current
        value held by each of the player's hands.
        """

        return "Player 1: {} - {}; Player 2: {} - {}".format(
            self.fingers['p1 left hand'], self.fingers['p1 right hand'],
            self.fingers['p2 left hand'], self.fingers['p2 right hand'])

    def __eq__(self, other) -> bool:
        """Compare two games of chopsticks and test for equality.
        """

        return type(self) == type(other) and self.player_one_turn \
            == other.player_one_turn and self.fingers == other.fingers

    def is_over(self, other) -> bool:
        """Return a boolean stating whether the chopsticks game is over.
        """

        if other.get_possible_moves() == []:
            return True
        return False

    def is_winner(self, player: str) -> bool:
        """Return a boolean stating if the current player is a winner of the
        chopsticks game.
        """

        if self.is_over(self.current_state):
            return self.current_state.get_current_player_name() != player
        else:
            return False


class ChopsticksState(CurrentState):
    """ A class to represent the state of a chopsticks game.
    ===Attributes===
    get_current_player_name: return a string representing the current player
    make_move: a method that makes a move chopsticks and creates a new
    game state.
    get_possible_moves: a method that returns the possible moves allowed to be
    played given a current game class.
    is_valid_move: a boolean method that checks if a move is valid.
    """
    def __init__(self, is_p1_turn: bool, fingers: Dict[str, int]) -> None:
        """Initialize the variables for a chopsticks game state.
        @param is_p1_turn a boolean that expresses whether it is player
        one's turn or not.
        @param fingers A dictionary representing the hands of both players and
        the values on each hand.
        """

        self.player_one_turn = is_p1_turn
        self.fingers = fingers

    def __str__(self):
        """Return a string representation of the current state of the game.
        """

        return "Player 1: {} - {}; Player 2: {} - {}".format\
            (self.fingers['p1 left hand'], self.fingers['p1 right hand'],
             self.fingers['p2 left hand'], self.fingers['p2 right hand'])

    def __eq__(self, other) -> bool:
        """Return whether current state self is equal to anoter current state.
        """

        return type(self) == type(other) and self.fingers == other.fingers \
            and self.player_one_turn == other.player_one_turn

    def dead_hand(self, fingers: Dict[str, int])-> Dict[str, int]:
        """Return a modified dictionary, where any key-value pairs that map
        to 5, will be reset to map to 0.
        """

        for finger in fingers:
            if fingers[finger] == 5:
                fingers[finger] = 0
        return fingers

    def over_five(self, fingers: Dict[str, int]) -> Dict[str, int]:
        """Return a modified dictionary, where any key-value pairs that map
        to values greater than 5, will be reset to map to 5 substracted from
        their value.
        """

        for finger in fingers:
            if fingers[finger] > 5:
                fingers[finger] -= 5
        return fingers

    def get_possible_moves(self) -> List[str]:
        """Return a list of string values representing the possible moves on
        the current state of the game.
        """

        length = 4
        possible_moves = []
        for finger in self.fingers:
            if self.fingers[finger] == 0:
                length -= 1

        if length == 4:
            possible_moves.extend(['ll', 'lr', 'rl', 'rr'])
        elif length <= 1:
            return possible_moves
        elif length == 3:
            possible_moves.extend(self.three_hand_moves())
        elif length == 2:
            possible_moves.extend(self.two_hand_moves())
        return possible_moves

    def three_hand_moves(self) -> List[str]:
        """Return a list of possible moves if three hands are still in play.
        """

        if self.player_one_turn:
            if self.fingers["p1 left hand"] == 0:
                return ['rl', 'rr']
            elif self.fingers["p1 right hand"] == 0:
                return ['ll', 'lr']
            elif self.fingers["p2 left hand"] == 0:
                return ['lr', 'rr']
            elif self.fingers["p2 right hand"] == 0:
                return ['ll', 'rl']
        else:
            if self.fingers["p1 left hand"] == 0:
                return ['lr', 'rr']
            elif self.fingers["p1 right hand"] == 0:
                return ['ll', 'rl']
            elif self.fingers["p2 left hand"] == 0:
                return ['rl', 'rr']
            elif self.fingers["p2 right hand"] == 0:
                return ['ll', 'lr']

    def two_hand_moves(self) -> List[str]:
        """Return a list of possible moves if only two hands are in play.
        """

        possible_moves = []
        if self.player_one_turn:
            if (self.fingers["p1 left hand"] == 0
            and self.fingers["p1 right hand"]) == 0:
                return possible_moves
            elif (self.fingers["p1 left hand"] == 0
                  and self.fingers["p2 right hand"]) == 0:
                possible_moves.append('rl')
            elif (self.fingers['p1 left hand'] == 0
                  and self.fingers['p2 left hand']) == 0:
                possible_moves.append('rr')
            elif (self.fingers['p2 left hand'] == 0
                  and self.fingers['p1 right hand']) == 0:
                possible_moves.append('lr')
            elif (self.fingers['p1 right hand'] == 0
                  and self.fingers['p2 right hand']) == 0:
                possible_moves.append('ll')
            elif (self.fingers['p2 left hand'] == 0
                  and self.fingers['p2 right hand']) == 0:
                return possible_moves
        else:
            if (self.fingers["p1 left hand"] == 0 and
            self.fingers["p1 right hand"]) == 0:
                return possible_moves
            elif (self.fingers["p1 left hand"] == 0 and
                  self.fingers["p2 right hand"]) == 0:
                possible_moves.append('lr')
            elif (self.fingers['p1 left hand'] == 0 and
                  self.fingers['p2 left hand']) == 0:
                possible_moves.append('rr')
            elif (self.fingers['p2 left hand'] == 0 and
                  self.fingers['p1 right hand']) == 0:
                possible_moves.append('rl')
            elif (self.fingers['p1 right hand'] == 0 and
                  self.fingers['p2 right hand']) == 0:
                possible_moves.append('ll')
            elif (self.fingers['p2 left hand'] == 0 and
                  self.fingers['p2 right hand']) == 0:
                return possible_moves
        return possible_moves

    def make_move(self, move_to_make: int)-> object:
        """Apply a move on the game and create a new current state of the game.
        """

        fingers = {}
        player_one_turn = self.player_one_turn

        for finger in self.fingers:
            fingers[finger] = self.fingers[finger]

        if self.is_valid_move(move_to_make):
            if self.player_one_turn:
                player_one_turn = False
                if move_to_make == "ll":
                    fingers['p2 left hand'] += fingers['p1 left hand']
                elif move_to_make == "lr":
                    fingers['p2 right hand'] += fingers['p1 left hand']
                elif move_to_make == "rl":
                    fingers['p2 left hand'] += fingers['p1 right hand']
                elif move_to_make == "rr":
                    fingers['p2 right hand'] += fingers['p1 right hand']
            elif not self.player_one_turn:
                player_one_turn = True
                if move_to_make == "ll":
                    fingers['p1 left hand'] += fingers['p2 left hand']
                elif move_to_make == "lr":
                    fingers['p1 right hand'] += fingers['p2 left hand']
                elif move_to_make == "rl":
                    fingers['p1 left hand'] += fingers['p2 right hand']
                elif move_to_make == "rr":
                    fingers['p1 right hand'] += fingers['p2 right hand']
            fingers = self.dead_hand(fingers)
            fingers = self.over_five(fingers)

        return ChopsticksState(player_one_turn, fingers)


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config="a1_pyta.txt")
