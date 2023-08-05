import unittest

# import numpy as np

from cli_tictactoe.main import TicTacToe


class TestGameBoard(unittest.TestCase):
    def test_board_dimension(self):
        """Board should be a 3x3 list"""
        game = TicTacToe()
        board = game.board
        assert len(board) == 3
        assert len(board[0]) == 3

    def test_board_initial_values(self):
        """All values in the beginning must be '-'"""
        game = TicTacToe()
        board = game.board
        for i in board:
            for j in i:
                assert j == "-"

    def test_x_player_choice(self):
        """Test x player choice"""
        game = TicTacToe()
        board = game.board
        game.x_player_choice(1, 2)
        assert board[1][2] == "x"

    def test_o_player_choice(self):
        """Test x player choice"""
        game = TicTacToe()
        board = game.board
        game.x_player_choice(2, 2)  # x player must go first
        game.o_player_choice(1, 2)
        assert board[1][2] == "o"

    def test_player_turn(self):
        """Test if the player turn logic is correct"""
        game = TicTacToe()
        game.x_player_choice(1, 2)
        assert game.turn_now == "o player"
        assert game.x_player_choice(0, 2) == -1
        assert game.o_player_choice(0, 2) == 0
        assert game.o_player_choice(0, 1) == -1

    def test_if_an_already_used_cell_is_not_overwritten(self):
        """Test to see if a player wont play in the same cell as the other"""
        game = TicTacToe()
        board = game.board
        game.x_player_choice(1, 2)
        game.o_player_choice(1, 2)
        assert board[1][2] == "x"
        game.o_player_choice(0, 2)
        game.x_player_choice(0, 2)
        assert board[0][2] == "o"

    def test_number_of_turns(self):
        """Test turns counter"""
        game = TicTacToe()
        game.x_player_choice(0, 0)
        game.o_player_choice(0, 1)
        assert game.turns == 2
        game.x_player_choice(0, 2)
        assert game.turns == 3
        game.o_player_choice(1, 0)
        game.x_player_choice(1, 1)
        game.o_player_choice(1, 2)
        assert game.turns == 6

    def test_game_status_winner_x_player_straight_column(self):
        """Test if a player is the winner every turn when n rounds >5"""
        game = TicTacToe()
        game.x_player_choice(0, 0)
        game.o_player_choice(0, 1)
        game.x_player_choice(1, 0)
        game.o_player_choice(0, 2)
        game.x_player_choice(2, 0)
        assert game.check_for_winner() == "x player"

    def test_game_status_winner_x_player_straight_row(self):
        """Test if a player is the winner every turn when n rounds >5"""
        game = TicTacToe()
        game.x_player_choice(2, 0)
        game.o_player_choice(0, 1)
        game.x_player_choice(2, 1)
        game.o_player_choice(0, 2)
        game.x_player_choice(2, 2)
        assert game.check_for_winner() == "x player"

    def test_game_status_winner_x_player_main_diagonal(self):
        """Test if a player is the winner every turn when n rounds >5"""
        game = TicTacToe()
        game.x_player_choice(0, 0)
        game.o_player_choice(0, 1)
        game.x_player_choice(1, 1)
        game.o_player_choice(0, 2)
        game.x_player_choice(2, 2)
        assert game.check_for_winner() == "x player"

    def test_game_status_winner_o_player_straight_column(self):
        """Test if a player is the winner every turn when n rounds >5"""
        game = TicTacToe()
        game.x_player_choice(0, 0)
        game.o_player_choice(0, 1)
        game.x_player_choice(1, 0)
        game.o_player_choice(1, 1)
        game.x_player_choice(2, 2)
        game.o_player_choice(2, 1)
        assert game.check_for_winner() == "o player"

    def test_game_status_winner_o_player_straight_row(self):
        """Test if a player is the winner every turn when n rounds >5"""
        game = TicTacToe()
        game.x_player_choice(0, 0)
        game.o_player_choice(1, 0)
        game.x_player_choice(2, 1)
        game.o_player_choice(1, 1)
        game.x_player_choice(2, 2)
        game.o_player_choice(1, 2)
        assert game.check_for_winner() == "o player"

    def test_game_status_winner_o_player_other_diagonal(self):
        """Test if a player is the winner every turn when n rounds >5"""
        game = TicTacToe()
        game.x_player_choice(0, 0)
        game.o_player_choice(0, 2)
        game.x_player_choice(1, 0)
        game.o_player_choice(1, 1)
        game.x_player_choice(2, 2)
        game.o_player_choice(2, 0)
        assert game.check_for_winner() == "o player"

    def test_game_status_tie(self):
        """Test if the game is tied"""
        game = TicTacToe()
        game.do_the_play(1, 1)
        game.do_the_play(0, 2)
        game.do_the_play(1, 2)
        game.do_the_play(1, 0)
        game.do_the_play(0, 1)
        game.do_the_play(2, 1)
        game.do_the_play(2, 2)
        game.do_the_play(0, 0)
        assert game.check_for_winner() == "tie"

    def test_new_game(self):
        """Tests if the new game was created right"""
        game = TicTacToe()
        game.do_the_play(1, 1)
        game.do_the_play(0, 2)
        game.do_the_play(1, 2)
        game.do_the_play(1, 0)
        game.do_the_play(0, 1)
        game.do_the_play(2, 1)
        game.do_the_play(2, 2)
        game.do_the_play(0, 0)
        game.new_game()
        board = game.board
        for i in board:
            for j in i:
                assert j == "-"
        assert game.turns == 0
        assert game.turn_now == "x player"
