"""
An implementation of a game of Stonehenge
"""

from typing import List, Any, Dict
from game import Game
from game_state import GameState

"""Dictionary constants to represent the Ley-Lines of each of the 5 
game boards."""

BOARD_1 = {1: ['@', 'A', 'B'], 2: ['@', 'C'], 3: ['@', 'C', 'A'], 4: ['@', 'B'],
           5: ['@', 'B', 'C'], 6: ['@', 'A']}

BOARD_2 = {1: ['@', 'A', 'B'], 2: ['@', 'C', 'D', 'E'], 3: ['@', 'F', 'G'],
           4: ['@', 'F', 'C'], 5: ['@', 'G', 'D', 'A'], 6: ['@', 'E', 'B'],
           7: ['@', 'E', 'G'], 8: ['@', 'B', 'D', 'F'], 9: ['@', 'A', 'C']}

BOARD_3 = {1: ['@', 'A', 'B'], 2: ['@', 'C', 'D', 'E'],
           3: ['@', 'F', 'G', 'H', 'I'], 4: ['@', 'J', 'K', 'L'],
           5: ['@', 'J', 'F'], 6: ['@', 'K', 'G', 'C'],
           7: ['@', 'L', 'H', 'D', 'A'], 8: ['@', 'E', 'B', 'I'],
           9: ['@', 'I', 'L'], 10: ['@', 'E', 'H', 'K'],
           11: ['@', 'B', 'D', 'G', 'J'], 12: ['@', 'A', 'C', 'F']}

BOARD_4 = {1: ['@', 'A', 'B'], 2: ['@', 'C', 'D', 'E'],
           3: ['@', 'F', 'G', 'H', 'I'], 4: ['@', 'J', 'K', 'L', 'M', 'N'],
           5: ['@', 'O', 'P', 'Q', 'R'], 6: ['@', 'O', 'J'],
           7: ['@', 'P', 'K', 'F'], 8: ['@', 'Q', 'L', 'G', 'C'],
           9: ['@', 'R', 'M', 'H', 'D', 'A'], 10: ['@', 'N', 'R'],
           11: ['@', 'I', 'M', 'Q'], 12: ['@', 'E', 'H', 'L', 'P'],
           13: ['@', 'B', 'D', 'G', 'K', 'O'], 14: ['@', 'A', 'C', 'F', 'J'],
           15: ['@', 'N', 'I', 'E', 'B']}

BOARD_5 = {1: ['@', 'A', 'B'], 2: ['@', 'C', 'D', 'E'],
           3: ['@', 'F', 'G', 'H', 'I'], 4: ['@', 'J', 'K', 'L', 'M', 'N'],
           5: ['@', 'O', 'P', 'Q', 'R', 'S', 'T'],
           6: ['@', 'U', 'V', 'W', 'X', 'Y'], 7: ['@', 'U', 'O'],
           8: ['@', 'V', 'P', 'J'], 9: ['@', 'W', 'Q', 'K', 'F'],
           10: ['@', 'X', 'R', 'L', 'G', 'C'],
           11: ['@', 'Y', 'S', 'M', 'H', 'D', 'A'], 12: ['@', 'T', 'Y'],
           13: ['@', 'N', 'S', 'X'], 14: ['@', 'I', 'M', 'R', 'W'],
           15: ['@', 'E', 'H', 'L', 'Q', 'V'],
           16: ['@', 'B', 'D', 'G', 'K', 'P', 'U'],
           17: ['@', 'A', 'C', 'F', 'J', 'O'],
           18: ['@', 'T', 'N', 'I', 'E', 'B']}


class StonehengeGame(Game):
    """
    A class to represent a Stonehenge game.
    """

    def __init__(self, p1_starts: bool) -> None:
        """
        Initialize the Stonehenge Game, using p1_starts to find who the first
        player is.
        """
        side_length = int(input("Enter the side length of the board "
                                "(must be between 1 to 5): "))
        if side_length == 1:
            self.tokens = {}
            for key in BOARD_1:
                self.tokens[key] = BOARD_1[key].copy()
        elif side_length == 2:
            self.tokens = {}
            for key in BOARD_2:
                self.tokens[key] = BOARD_2[key].copy()
        elif side_length == 3:
            self.tokens = {}
            for key in BOARD_3:
                self.tokens[key] = BOARD_3[key].copy()
        elif side_length == 4:
            self.tokens = {}
            for key in BOARD_4:
                self.tokens[key] = BOARD_4[key].copy()
        else:
            self.tokens = {}
            for key in BOARD_5:
                self.tokens[key] = BOARD_5[key].copy()
        self.current_state = StonehengeState(p1_starts, side_length,
                                             self.tokens)

    def get_instructions(self) -> str:
        """
        Return the instructions for this a Stonehenge Game.
        """
        return "Players take turns claiming cells from the following game " \
               "board. \nA player that has claimed at least half of the cells" \
               " in a ley-line, will capture that ley-line. \nOnce a cell or " \
               "ley-line are claimed, the other player cannot capture either." \
               " \nThe first player to capture at least half of the ley-lines" \
               " on the game board is the winner."

    def is_over(self, state: GameState) -> bool:
        """
        Return whether or not this Stonehenge game is over at state.
        """
        return state.get_possible_moves() == []

    def is_winner(self, player: str) -> bool:
        """
        Return whether player has won the game.

        Precondition: player is 'p1' or 'p2'.
        """
        return (self.current_state.get_current_player_name() != player
                and self.is_over(self.current_state))

    def str_to_move(self, string: str) -> Any:
        """
        Return the move that string represents. If string is not a move,
        return some invalid move.
        """
        string.strip()
        if len(string) != 1 or type(string) != str or string.islower():
            return -1
        return str(string)


class StonehengeState(GameState):
    """
    The state of a Stonehenge game at a certain point in time.
    """

    def __init__(self, is_p1_turn: bool, side_length: int,
                 tokens: Dict[int, List[str]]) -> None:
        """
        Initialize this game state and set the current player based on
        is_p1_turn.

        """
        super().__init__(is_p1_turn)
        self.side_length = side_length
        self.tokens = tokens
        if side_length == 1:
            self.board = \
                """\
                  {}   {}
                 /   /
            {} - {} - {}
                 \\ / \\
              {} - {}   {}
                   \\
                    {}""".format(self.tokens[6][0], self.tokens[5][0],
                                 self.tokens[1][0], self.tokens[1][1],
                                 self.tokens[1][2], self.tokens[2][0],
                                 self.tokens[2][1], self.tokens[4][0],
                                 self.tokens[3][0])
        elif side_length == 2:
            self.board = \
                """\
                    {}   {}
                   /   /
              {} - {} - {}   {}
                 / \\ / \\ /
            {} - {} - {} - {}
                 \\ / \\ / \\
              {} - {} - {}   {}
                   \\   \\
                    {}   {}""".format(self.tokens[9][0], self.tokens[8][0],
                                      self.tokens[1][0], self.tokens[1][1],
                                      self.tokens[1][2], self.tokens[7][0],
                                      self.tokens[2][0], self.tokens[2][1],
                                      self.tokens[2][2], self.tokens[2][3],
                                      self.tokens[3][0], self.tokens[3][1],
                                      self.tokens[3][2], self.tokens[6][0],
                                      self.tokens[4][0], self.tokens[5][0])

        elif side_length == 3:
            self.board = \
                """\
                      {}   {}
                     /   /
                {} - {} - {}   {}
                   / \\ / \\ /
              {} - {} - {} - {}   {}
                 / \\ / \\ / \\ /
            {} - {} - {} - {} - {}
                 \\ / \\ / \\ / \\
              {} - {} - {} - {}   {}
                   \\   \\   \\
                    {}   {}   {}""".format(self.tokens[12][0],
                                           self.tokens[11][0],
                                           self.tokens[1][0],
                                           self.tokens[1][1],
                                           self.tokens[1][2],
                                           self.tokens[10][0],
                                           self.tokens[2][0],
                                           self.tokens[2][1],
                                           self.tokens[2][2],
                                           self.tokens[2][3],
                                           self.tokens[9][0],
                                           self.tokens[3][0],
                                           self.tokens[3][1],
                                           self.tokens[3][2],
                                           self.tokens[3][3],
                                           self.tokens[3][4],
                                           self.tokens[4][0],
                                           self.tokens[4][1],
                                           self.tokens[4][2],
                                           self.tokens[4][3],
                                           self.tokens[8][0],
                                           self.tokens[5][0],
                                           self.tokens[6][0],
                                           self.tokens[7][0])

        elif side_length == 4:
            self.board = \
                """\
                        {}   {}
                       /   /
                  {} - {} - {}   {}
                     / \\ / \\ /
                {} - {} - {} - {}   {}
                   / \\ / \\ / \\ /
              {} - {} - {} - {} - {}   {}
                 / \\ / \\ / \\ / \\ /
            {} - {} - {} - {} - {} - {} 
                 \\ / \\ / \\ / \\ / \\
              {} - {} - {} - {} - {}   {}
                   \\   \\   \\   \\
                    {}   {}   {}   {}""".format(self.tokens[14][0],
                                                self.tokens[13][0],
                                                self.tokens[1][0],
                                                self.tokens[1][1],
                                                self.tokens[1][2],
                                                self.tokens[12][0],
                                                self.tokens[2][0],
                                                self.tokens[2][1],
                                                self.tokens[2][2],
                                                self.tokens[2][3],
                                                self.tokens[11][0],
                                                self.tokens[3][0],
                                                self.tokens[3][1],
                                                self.tokens[3][2],
                                                self.tokens[3][3],
                                                self.tokens[3][4],
                                                self.tokens[10][0],
                                                self.tokens[4][0],
                                                self.tokens[4][1],
                                                self.tokens[4][2],
                                                self.tokens[4][3],
                                                self.tokens[4][4],
                                                self.tokens[4][5],
                                                self.tokens[5][0],
                                                self.tokens[5][1],
                                                self.tokens[5][2],
                                                self.tokens[5][3],
                                                self.tokens[5][4],
                                                self.tokens[15][0],
                                                self.tokens[6][0],
                                                self.tokens[7][0],
                                                self.tokens[8][0],
                                                self.tokens[9][0])
        else:
            self.board = \
                """\
                          {}   {}
                         /   /
                    {} - {} - {}   {}           
                       / \\ / \\ /
                  {} - {} - {} - {}   {}
                     / \\ / \\ / \\ /
                {} - {} - {} - {} - {}   {}
                   / \\ / \\ / \\ / \\ /
              {} - {} - {} - {} - {} - {}   {}
                 / \\ / \\ / \\ / \\ / \\ /
            {} - {} - {} - {} - {} - {} - {}
                 \\ / \\ / \\ / \\ / \\ / \\
              {} - {} - {} - {} - {} - {}   {} 
                   \\   \\   \\   \\   \\
                    {}   {}   {}   {}   {}""".format(self.tokens[17][0],
                                                     self.tokens[16][0],
                                                     self.tokens[1][0],
                                                     self.tokens[1][1],
                                                     self.tokens[1][2],
                                                     self.tokens[15][0],
                                                     self.tokens[2][0],
                                                     self.tokens[2][1],
                                                     self.tokens[2][2],
                                                     self.tokens[2][3],
                                                     self.tokens[14][0],
                                                     self.tokens[3][0],
                                                     self.tokens[3][1],
                                                     self.tokens[3][2],
                                                     self.tokens[3][3],
                                                     self.tokens[3][4],
                                                     self.tokens[13][0],
                                                     self.tokens[4][0],
                                                     self.tokens[4][1],
                                                     self.tokens[4][2],
                                                     self.tokens[4][3],
                                                     self.tokens[4][4],
                                                     self.tokens[4][5],
                                                     self.tokens[12][0],
                                                     self.tokens[5][0],
                                                     self.tokens[5][1],
                                                     self.tokens[5][2],
                                                     self.tokens[5][3],
                                                     self.tokens[5][4],
                                                     self.tokens[5][5],
                                                     self.tokens[5][6],
                                                     self.tokens[6][0],
                                                     self.tokens[6][1],
                                                     self.tokens[6][2],
                                                     self.tokens[6][3],
                                                     self.tokens[6][4],
                                                     self.tokens[6][5],
                                                     self.tokens[18][0],
                                                     self.tokens[7][0],
                                                     self.tokens[8][0],
                                                     self.tokens[9][0],
                                                     self.tokens[10][0],
                                                     self.tokens[11][0])

    def __str__(self) -> str:
        """
        Return a string representation of the current state of the game.
        """
        return self.board

    def get_possible_moves(self) -> list:
        """
        Return all possible moves that can be applied to this state.
        """
        possible_moves = []
        # check if a game is over
        if self.p1_turn:
            count = 0
            for ley_line in self.tokens:
                if self.tokens[ley_line][0] == '2':
                    count += 1
            if count >= (len(self.tokens) / 2):
                return possible_moves
        else:
            count = 0
            for ley_line in self.tokens:
                if self.tokens[ley_line][0] == '1':
                    count += 1
            if count >= (len(self.tokens) / 2):
                return possible_moves

        # if game is not over then get possible moves
        for ley_line in self.tokens:
            for token in self.tokens[ley_line]:
                if token != '@' and token != '1' and token != '2' and token not\
                        in possible_moves:
                    possible_moves.append(token)
        return possible_moves

    def make_move(self, move: Any) -> 'GameState':
        """
        Return the GameState that results from applying move to this GameState.
        """
        tokens = {}
        for key in self.tokens:
            tokens[key] = self.tokens[key].copy()
        if self.p1_turn:
            new_token = '1'
        else:
            new_token = '2'

        for ley_line in tokens:
            for i in range(len(tokens[ley_line])):
                if tokens[ley_line][i] == move:
                    tokens[ley_line][i] = new_token

        for ley_line in tokens:
            count = 0
            for i in range(len(tokens[ley_line])):
                if tokens[ley_line][i] == new_token:
                    count += 1
            if count >= ((len(tokens[ley_line]) - 1)/2) \
                    and tokens[ley_line][0] == '@':
                tokens[ley_line][0] = new_token
        if self.p1_turn:
            return StonehengeState(False, self.side_length, tokens)
        return StonehengeState(True, self.side_length, tokens)

    def __repr__(self) -> Any:
        """
        Return a representation of this state (which can be used for
        equality testing).
        """
        if self.p1_turn:
            representation = "It is currently player one's turn and the state" \
                             " of the game is {}".format(self.board)
        else:
            representation = "It is currently player two's turn and the state" \
                             " of the game is {}".format(self.board)
        return representation

    def rough_outcome(self) -> float:
        """
        Return an estimate in interval [LOSE, WIN] of best outcome the current
        player can guarantee from state self.
        """
        player_points = []

        for move in self.get_possible_moves():
            new_state = self.make_move(move)
            if new_state.get_possible_moves() == []:
                return 1
            else:
                for move2 in new_state.get_possible_moves():
                    new_state_2 = new_state.make_move(move2)
                    player_points = [-1 if new_state_2.get_possible_moves()
                                     == [] else 0]
        if all(player_points):
            return -1
        return 0


if __name__ == '__main__':
    from python_ta import check_all
    check_all(config="a2_pyta.txt")
