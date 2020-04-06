"""
Tic Tac Toe Player
"""

import math, collections, operator
from copy import deepcopy

import numpy as np


X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    
    
    The player function should take a board state as
    input, and return which player’s turn it is (either 
    X or O). In the initial game state, X gets the
    first move. Subsequently, the player alternates
    with each additional move. Any return value is 
    acceptable if a terminal board is provided as 
    input (i.e., the game is already over).

    """
    flat_board = [c for row in board for c in row]
    counter = collections.Counter(flat_board)
    if counter[None]== 0:
        return "full board"
    elif counter[None]==9:
        return X
    del counter[None]
    return X if counter[X]<=counter[O] else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    
    The actions function should return a set of all of the
    possible actions that can be taken on a given board.
    Each action should be represented as a tuple (i, j) 
    where i corresponds to the row of the move (0, 1, or 2) 
    and j corresponds to which cell in the row corresponds 
    to the move (also 0, 1, or 2).
    Possible moves are any cells on the board that do not 
    already have an X or an O in them.
    Any return value is acceptable if a terminal board is 
    provided as input.
    
    """
    actions = set()
    for i, row in enumerate(board):
        for j, val in enumerate(row):
            if val==EMPTY:
                actions.add((i,j))
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    
    The result function takes a board and an action as input,
    and should return a new board state, without modifying the
    original board.

    If action is not a valid action for the board, your program
    should raise an exception.
    The returned board state should be the board that would 
    result from taking the original input board, and letting 
    the player whose turn it is make their move at the cell 
    indicated by the input action.
    Importantly, the original board should be left unmodified:
    since Minimax will ultimately require considering many different
    board states during its computation. This means that simply
    updating a cell in board itself is not a correct implementation 
    of the result function. You’ll likely want to make a deep 
    copy of the board first before making any changes.
    
    """
    if action not in actions(board):
        raise ValueError("action passed ", action,
                         " is not in allowed actions ",
                         actions(board), " for ", board)
    new_board = deepcopy(board)
    player_XO = player(board)
    row, col = action
    new_board[row][col] = player_XO
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    
    The winner function should accept a board as input,
    and return the winner of the board if there is one.

    If the X player has won the game, your function should 
    return X. If the O player has won the game, your 
    function should return O.
    One can win the game with three of their moves in a
    row horizontally, vertically, or diagonally.
    You may assume that there will be at most one winner
    (that is, no board will ever have both players with 
    three-in-a-row, since that would be an invalid board 
    state).
    If there is no winner of the game (either because the
    game is in progress, or because it ended in a tie), 
    the function should return None.

    """
    import numpy as np
    aboard = np.array(board)
    
    for X_or_O in (X, O):
        col = np.any(np.sum(aboard==X_or_O, axis=0)==3)
        li = np.any(np.sum(aboard==X_or_O, axis=1)==3)
        diag = np.sum(np.diag(aboard==X_or_O))==3
        diag_t = np.sum(np.diag(np.fliplr(aboard))==X_or_O)==3
        if col or li or diag or diag_t:
            return X_or_O
    return 0


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    
    The terminal function should accept a board as 
    input, and return a boolean value indicating whether
    the game is over.

    If the game is over, either because someone has won 
    the game or because all cells have been filled without
    anyone winning, the function should return True.
    Otherwise, the function should return False if the 
    game is still in progress.

    """
    if winner(board) is not 0 or bool(actions(board)) == False:
        return True
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    
    The utility function should accept a terminal board as
    input and output the utility of the board.

    If X has won the game, the utility is 1. If O has won
    the game, the utility is -1. If the game has ended in 
    a tie, the utility is 0.
    You may assume utility will only be called on a board 
    if terminal(board) is True.
    
    """
    #if not terminal(board):
    #    raise ValueError('Board should be terminal to compute its utility')
    if winner(board)==X:
        return 1
    elif winner(board)==O:
        return -1
    else:
        return 0


def minimax_value(board):
    """
    Return only the minimax value of the board.
    Not the action.
    """
    if terminal(board):
        return utility(board)
    
    # initialize values
    init = 2
    board_actions = actions(board)
    player_X_or_O = player(board)
    # set player functions
    if player_X_or_O==X:
        func = max
        v = -init
    elif player_X_or_O==O:
        func = min
        v = init
    else:
        raise ValueError("Player is", player_X_or_O)
    
    # Computation of minimax value : 
    # for all actions, compute the minimax value...
    for action in board_actions:
        next_board = result(board, action)
        res = minimax_value(next_board)
        # and update when a better solution is found
        # according to the min/max function
        v = func(v, res)
    return v
        
def minimax_value_alpha_beta(board, alpha, beta):
    if terminal(board):
        return utility(board)

    # initialize values
    init = 2
    board_actions = actions(board)
    player_X_or_O = player(board)
    # set player functions
    if player_X_or_O==X:
        func = max
        v = -init
    elif player_X_or_O==O:
        func = min
        v = init
    else:
        raise ValueError("Player is", player_X_or_O)
        
    # Computation of minimax value : 
    # for all actions, compute the minimax value...
    for action in board_actions:
        next_board = result(board, action)
        res = minimax_value_alpha_beta(next_board, alpha, beta)
        # and update when a better solution is found
        # according to the min/max function
        v = func(v, res)
        if player_X_or_O==X:
            alpha = max(alpha, res)
            if beta <= alpha:
                break
        elif player_X_or_O==O:
            beta = min(beta, res)
            if alpha >= beta:
                break
        else:
            raise ValueError("Player is", player_X_or_O)
    return v


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    
    The minimax function should take a board as input, 
    and return the optimal move for the player to move on that board.

    The move returned should be the optimal action (i, j) 
    that is one of the allowable actions on the board. 
    If multiple moves are equally optimal, any of those
    moves is acceptable.
    If the board is a terminal board, the minimax function
    should return None.

    """
    # If TERMINAL, no best move
    if terminal(board):
        return None
    # initialize values
    init = 2
    board_actions = actions(board)
    player_X_or_O = player(board)
    alpha = -init
    beta = +init
    
    # we want to compute and update the best action from this point
    best_action = None

    # set player functions
    if player_X_or_O==X:
        func = max
        v = -init
        op = operator.gt
    elif player_X_or_O==O:
        func = min
        v = init
        op = operator.lt
    else:
        raise ValueError("Player is", player_X_or_O)    

    # Computation of minimax best action : 
    # for all actions, compute the minimax value... 
    for action in board_actions:
        # Compute minimax value for next board
        next_board = result(board, action)
        res = minimax_value_alpha_beta(next_board, alpha, beta)
        #res = minimax_value(next_board)
        # save the action if the score is the best so far
        if op(res, v):
            best_action = action
        # and update the best score so far
        v = func(v, res)
    return best_action
