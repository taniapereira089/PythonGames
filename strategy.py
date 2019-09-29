"""
A module for strategies.

NOTE: Make sure this file adheres to python-ta.
Adjust the type annotations as needed, and implement both a recursive
and an iterative version of minimax.
"""
from typing import Any

# TODO: Adjust the type annotation as needed.


def interactive_strategy(game: Any) -> Any:
    """
    Return a move for game through interactively asking the user for input.
    """
    move = input("Enter a move: ")
    return game.str_to_move(move)


def rough_outcome_strategy(game: Any) -> Any:
    """
    Return a move for game by picking a move which results in a state with
    the lowest rough_outcome() for the opponent.

    NOTE: game.rough_outcome() should do the following:
        - For a state that's over, it returns the score for the current
          player of that state.
        - For a state that's not over:
            - If there is a move that results in the current player winning,
              return 1.
            - If all moves result in states where the other player can
              immediately win, return -1.
            - Otherwise; return a number between -1 and 1 corresponding to how
              'likely' the current player will win from the current state.

        In essence: rough_outcome() will only look 1 or 2 states ahead to
        'guess' the outcome of the game, but no further. It's better than
        random, but worse than minimax.
    """
    current_state = game.current_state
    best_move = None
    best_outcome = -2

    # Get the move that results in the lowest rough_outcome for the opponent
    for move in current_state.get_possible_moves():
        new_state = current_state.make_move(move)

        # We multiply the below by -1 since a state that's bad for the opponent
        # is good for us.
        guessed_score = new_state.rough_outcome() * -1
        if guessed_score > best_outcome:
            best_outcome = guessed_score
            best_move = move

    # Return the move that resulted in the best rough_outcome
    return best_move

# TODO: Implement a recursive version of the minimax strategy.


def recursive_minimax_strategy(game: Any) -> Any:
    """
    Return a move for a game generated using the minimax strategy.
    This implementation will use recursion.
    """
    current_state = game.current_state
    initial_moves = {1: [], -1: [], 0: []}
    for move in current_state.get_possible_moves():
        new_state = current_state.make_move(move)
        initial_moves[-1 * recursive_helper(game, new_state)].append(move)
        game.current_state = current_state
    if initial_moves[1] != []:
        return initial_moves[1][0]
    elif initial_moves[0] != []:
        return initial_moves[0][0]
    return initial_moves[-1][0]


def recursive_helper(game: Any, state: Any) -> int:
    """
    Return the score that a potential move will have for the player.
    """
    game.current_state = state
    if state.get_current_player_name() == 'p1':
        current_player = 'p1'
        opponent = 'p2'
    else:
        current_player = 'p2'
        opponent = 'p1'

    if game.is_over(state):
        if game.is_winner(current_player):
            return 1
        elif game.is_winner(opponent):
            return -1
        return 0
    else:
        return max([recursive_helper(game, state.make_move(move)) * -1
                    for move in state.get_possible_moves()])


# TODO: Implement an iterative version of the minimax strategy.


def iterative_minimax_strategy(game: Any) -> Any:
    """
    Return a move for a game generated using the minimax strategy.
    This implementation will not include recursion.
    """
    state = game.current_state
    s = Stack()
    possible_moves = {}
    initial_item = PotentialState(state)
    s.add(initial_item)

    while not s.is_empty():
        item = s.remove()
        game.current_state = item.value
        if item.children == []:
            if game.is_over(item.value):
                if item.value.p1_turn:
                    current_player = 'p1'
                    opponent = 'p2'
                else:
                    current_player = 'p2'
                    opponent = 'p1'
                if game.is_winner(current_player):
                    item.score = 1
                elif game.is_winner(opponent):
                    item.score = -1
                else:
                    item.score = 0
            else:
                s.add(item)
                for move in item.value.get_possible_moves():
                    new_state = item.value.make_move(move)
                    new_item = PotentialState(new_state)
                    item.children.append(new_item)
                    possible_moves[new_state] = move
                    s.add(new_item)
        else:
            child_scores = []
            for child in item.children:
                child_scores.append(child.score * -1)
            item.score = max(child_scores)

    game.current_state = state
    for child in initial_item.children:
        if child.score == -1:
            return possible_moves[child.value]
    for child in initial_item.children:
        if child.score == 0:
            return possible_moves[child.value]
    dict_keys = []
    for key in possible_moves:
        dict_keys.append(key)
    return possible_moves[dict_keys[0]]


class PotentialState:
    """
    A class to represent a potential state of a game based on if a move was
    made, and its children of the same data structure.
    """
    def __init__(self, value: Any, children=None, score=None):
        """
        Initialize a new potential state of a game to keep track of its
        children, which are the states of the game made with each possible
        move on this potential state.
        """
        self.value = value
        self.children = children[:] if children is not None else []
        self.score = score


class Stack:
    """ Last-in, first-out (LIFO) stack.
    """

    def __init__(self) -> None:
        """ Create a new, empty Stack self.

        >>> s = Stack()
        """
        self._contains = []

    def add(self, obj: object) -> None:
        """ Add object obj to top of Stack self.

        >>> s = Stack()
        >>> s.add(5)
        """
        self._contains.append(obj)

    def remove(self) -> object:
        """
        Remove and return top element of Stack self.

        Assume Stack self is not emp.

        >>> s = Stack()
        >>> s.add(5)
        >>> s.add(7)
        >>> s.remove()
        7
        """
        return self._contains.pop()

    def is_empty(self) -> bool:
        """
        Return whether Stack self is empty.

        >>> s = Stack()
        >>> s.is_empty()
        True
        >>> s.add(5)
        >>> s.is_empty()
        False
        """
        return len(self._contains) == 0


if __name__ == "__main__":
    from python_ta import check_all

    check_all(config="a2_pyta.txt")
