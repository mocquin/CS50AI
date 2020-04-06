import unittest

from tictactoe import X, O, EMPTY
from tictactoe import initial_state, player, actions, result, winner, terminal, utility, minimax_value, minimax_value_alpha_beta


class TestTictactoe(unittest.TestCase):
    

    def test_00_initial_state(self):
        # We expect the initial state to be a 3x3 list filled 
        # with EMPTY values
        self.assertEqual(initial_state(),
                         [[EMPTY, EMPTY, EMPTY],
                          [EMPTY, EMPTY, EMPTY],
                          [EMPTY, EMPTY, EMPTY],])
        
    def test_10_player(self):
        
        # X player starts
        board_init = [[EMPTY, EMPTY, EMPTY],
                      [EMPTY, EMPTY, EMPTY],
                      [EMPTY, EMPTY, EMPTY]]
        self.assertEqual(player(board_init), 
                         X)
        # turn to X
        board_X = [[X, EMPTY, EMPTY],
                   [O, EMPTY, EMPTY],
                   [EMPTY, EMPTY, EMPTY]]
        self.assertEqual(player(board_X), 
                         X)
        
        # turn to O
        board_O = [[X, X, EMPTY],
                   [O, EMPTY, EMPTY],
                   [EMPTY, EMPTY, EMPTY]]
        self.assertEqual(player(board_O), 
                         O)
    
        # terminal board : must not raise exception
        # X winner
        board_X_win = [[X, X, X],
                       [O, O, EMPTY],
                       [EMPTY, EMPTY, EMPTY]]
        try:
            player(board_X_win)
        except e as e:
            self.fail()
        
        # O winner
        board_O_win = [[X, X, EMPTY],
                       [O, O, O],
                       [X, EMPTY, EMPTY]]
        try:
            player(board_O_win)
        except e as e:
            self.fail()
            
        # tie
        board_tie = [[X, X, O],
                     [O, O, X],
                     [X, O, X]]
        try:
            player(board_tie)
        except e as e:
            self.fail()
            
    def test_20_actions(self):
        
        # empty board
        empty_board = [[EMPTY, EMPTY, EMPTY],
                      [EMPTY, EMPTY, EMPTY],
                      [EMPTY, EMPTY, EMPTY]]
        self.assertEqual(actions(empty_board),
                         set(((0,0), (0,1), (0,2),
                            (1,0), (1,1), (1,2),
                            (2,0), (2,1), (2,2))))
        
        # full board
        full_board = [[X, X, O],
                     [O, O, X],
                     [X, O, X]]
        try:
            actions(full_board)
        except e as e:
            self.fail()
            
        # random board 1
        board_X = [[X, EMPTY, EMPTY],
                   [O, EMPTY, EMPTY],
                   [EMPTY, EMPTY, EMPTY]]
        self.assertEqual(actions(board_X),
                        set(((0, 1), (0, 2), 
                            (1, 1), (1, 2),
                            (2, 0), (2,1), (2, 2))))
        
        # random board 2
        board_O = [[X, X, EMPTY],
                   [O, EMPTY, EMPTY],
                   [EMPTY, EMPTY, EMPTY]]
        self.assertEqual(actions(board_O),
                         set(((0, 2), 
                             (1, 1), (1, 2),
                             (2, 0), (2,1), (2, 2))))
        
    def test_30_result(self):
        
        # raise exception if not valid action
        board = [[X, X, EMPTY],
                 [O, EMPTY, EMPTY],
                 [EMPTY, EMPTY, EMPTY]]
        with self.assertRaises(ValueError):
            result(board,(0, 0))
        
        # X turn
        board_X = [[X, X, EMPTY],
                 [O, EMPTY, EMPTY],
                 [EMPTY, EMPTY, EMPTY]]
        self.assertEqual(result(board_X, (1, 1)),
                        [[X, X, EMPTY],
                         [O, O, EMPTY],
                         [EMPTY, EMPTY, EMPTY]])
        
        # O turn
        board_O = [[X, X, EMPTY],
                   [O, EMPTY, EMPTY],
                   [EMPTY, EMPTY, EMPTY]]
        self.assertEqual(result(board_O, (0, 2)),
                        [[X, X, O],
                         [O, EMPTY, EMPTY],
                         [EMPTY, EMPTY, EMPTY]])
        
    def test_40_winner(self):
        
        # no winner
        board_O = [[X, X, EMPTY],
                   [O, EMPTY, EMPTY],
                   [EMPTY, EMPTY, EMPTY]]
        self.assertEqual(winner(board_O), 
                        0)
        # no winner
        board_X = [[X, X, EMPTY],
                   [O, O, EMPTY],
                   [EMPTY, EMPTY, EMPTY]]
        self.assertEqual(winner(board_X),
                        0)
        
        # tie
        board_tie = [[X, X, O],
                   [O, O, X],
                   [X, O, X]]
        self.assertEqual(winner(board_X),
                        0)
        
        # line
        board_X = [[X, X, X],
                   [O, O, EMPTY],
                   [EMPTY, EMPTY, EMPTY]]
        self.assertEqual(winner(board_X),
                        X)
        
        # col
        board_X = [[X, O, X],
                   [X, O, O],
                   [X, EMPTY, EMPTY]]
        self.assertEqual(winner(board_X),
                        X)
        
        # first diag
        board_diag1 = [[X, X, O],
                       [X, X, O],
                       [O, O, X]]
        self.assertEqual(winner(board_X),
                        X)
        # other diag
        board_diag2 = [[O, O, X],
                       [X, X, O],
                       [X, O, X]]
        self.assertEqual(winner(board_X),
                        X)
        
    def test_50_terminal(self):
        
        board_diag2 = [[O, O, X],
                       [X, X, O],
                       [X, O, X]]
        self.assertEqual(terminal(board_diag2), True)
        
        board_diag1 = [[X, X, O],
                       [X, X, O],
                       [O, O, X]]
        self.assertEqual(terminal(board_diag1), True)
                        
        board = [[X, X, EMPTY],
                 [O, O, EMPTY],
                 [EMPTY, EMPTY, EMPTY]]
        self.assertEqual(terminal(board),
                        False)

        board = [[EMPTY, EMPTY, EMPTY],
                 [EMPTY, EMPTY, EMPTY],
                 [EMPTY, EMPTY, EMPTY]]
        self.assertEqual(terminal(board), False)
                         
    def test_60_utility(self):
        
        # utility is 1 when X is winner
        board_diag1 = [[X, X, O],
                       [X, X, O],
                       [O, O, X]]        
        self.assertEqual(utility(board_diag1),
                        1)

        # utility is 1 when X is winner
        board_diag2 = [[O, O, X],
                       [X, X, O],
                       [X, O, X]]       
        self.assertEqual(utility(board_diag2),
                        1)
        
        # game not finished
        board = [[EMPTY, EMPTY, EMPTY],
                 [EMPTY, EMPTY, EMPTY],
                 [EMPTY, EMPTY, EMPTY]]
        self.assertEqual(utility(board),
                        0)
        
        # game not finished
        board = [[X, X, EMPTY],
                 [O, O, EMPTY],
                 [EMPTY, EMPTY, EMPTY]]
        self.assertEqual(utility(board),
                        0)
        
        # O wins
        board = [[X, X, EMPTY],
                 [O, O, O],
                 [X, EMPTY, EMPTY]]
        self.assertEqual(utility(board),
                        -1)
        
        # tie
        board_tie = [[X, X, O],
                   [O, O, X],
                   [X, O, X]]
        self.assertEqual(utility(board_tie),
                        0)
        
    def test_70_alpha_beta_pruning(self):
        boards = [
            [[EMPTY, EMPTY, EMPTY],
             [EMPTY, EMPTY, EMPTY],
             [EMPTY, EMPTY, EMPTY]],
            [[X, X, O],
             [O, O, X],
             [X, O, X]],
            [[X, X, EMPTY],
             [O, O, O],
             [X, EMPTY, EMPTY]],
            [[X, X, EMPTY],
             [O, O, EMPTY],
             [EMPTY, EMPTY, EMPTY]],
            [[O, O, X],
             [X, X, O],
             [X, O, X]],
        ]
        for board in boards:
            self.assertEqual(minimax_value(board),
                            minimax_value_alpha_beta(board, -2, 2))