#!/usr/bin/env python3
# from os import path

# import numpy as np


class TablePrinter(object):
    "Print a list of dicts as a table"

    def __init__(self, fmt, sep=" ", ul=None):
        """
        @param fmt: list of tuple(heading, key, width)
                        heading: str, column label
                        key: dictionary key to value to print
                        width: int, column width in chars
        @param sep: string, separation between columns
        @param ul: string, character to underline column label, or None for no underlining
        """
        super(TablePrinter, self).__init__()
        self.fmt = str(sep).join(
            "{lb}{0}:{1}{rb}".format(key, width, lb="{", rb="}")
            for heading, key, width in fmt
        )
        self.head = {key: heading for heading, key, width in fmt}
        self.ul = {key: str(ul) * width for heading, key, width in fmt} if ul else None
        self.width = {key: width for heading, key, width in fmt}

    def row(self, data):
        return self.fmt.format(
            **{k: str(data.get(k, ""))[:w] for k, w in self.width.items()}
        )

    def __call__(self, dataList):
        _r = self.row
        res = [_r(data) for data in dataList]
        res.insert(0, _r(self.head))
        if self.ul:
            res.insert(1, _r(self.ul))
        return "\n".join(res)


class TicTacToe:
    """Class to TicTacToe game"""

    def __init__(self):
        self.init_board()
        self.turn_now = "x player"
        self.turns = 0

    def init_board(self) -> list:
        """Defines the initial board"""
        self.board = [["-" for j in range(3)] for i in range(3)]
        return self.board

    def player_turn(self, turn_now: str) -> str:
        """return the current player turn, also increase the turns counter"""
        self.turns += 1
        if turn_now == "x":
            return "o player"
        return "x player"

    def x_player_choice(self, x_pos: int, y_pos: int) -> int:
        """Computes x_player_choice"""
        if self.turn_now == "x player" and self.board[x_pos][y_pos] == "-":
            self.board[x_pos][y_pos] = "x"
            self.turn_now = self.player_turn("x")
            return 0
        return -1

    def o_player_choice(self, x_pos: int, y_pos: int) -> int:
        """Computes x_player_choice"""
        if self.turn_now == "o player" and self.board[x_pos][y_pos] == "-":
            self.board[x_pos][y_pos] = "o"
            self.turn_now = self.player_turn("y")
            return 0
        return -1

    def do_the_play(self, x_pos: int, y_pos: int) -> int:
        """Function to wrap the play"""
        if self.turn_now == "x player":
            return self.x_player_choice(x_pos, y_pos)
        elif self.turn_now == "o player":
            return self.o_player_choice(x_pos, y_pos)

    def check_for_winner(self):
        """Check for a winner if the number of turns is >= 5"""
        if self.turns >= 5:
            if self.turns == 8:
                board_now = [["x" if i == "-" else i for i in j] for j in self.board]
            else:
                board_now = self.board
            first_line = board_now[0]
            second_line = board_now[1]
            third_line = board_now[2]
            transpose = list(map(list, zip(*board_now)))
            first_column = transpose[0]
            second_column = transpose[1]
            third_column = transpose[2]
            main_diagonal = [board_now[0][0], board_now[1][1], board_now[2][2]]
            other_diagonal = [board_now[2][0], board_now[1][1], board_now[0][2]]
            all_possibilities = [
                first_line,
                second_line,
                third_line,
                first_column,
                second_column,
                third_column,
                main_diagonal,
                other_diagonal,
            ]
            for possibility in all_possibilities:
                if "-" in possibility:
                    continue
                if "x" in possibility and "o" not in possibility:
                    return "x player"
                if "o" in possibility and "x" not in possibility:
                    return "o player"

            n_possibility = 0  # Flag to tell the number of possibilities already tested
            for possibility in all_possibilities:
                if "x" in possibility and "o" in possibility:
                    n_possibility += 1
                if n_possibility == 8:
                    return "tie"
            return None

    def new_game(self):
        self.init_board()
        self.turn_now = "x player"
        self.turns = 0

    def __str__(self):
        """Print the game in a pretty way"""
        center1 = "|{:^7}"
        center2 = "{:^7}"
        center3 = "{:^7}|"
        fmt1 = [
            ("", "ident", 15),
            ("", "col1", 8),
            ("", "col2", 8),
            ("", "col3", 8),
        ]

        data1 = [
            {
                "ident": "",
                "col1": center1.format(self.board[0][0]),
                "col2": center2.format(self.board[0][1]),
                "col3": center3.format(self.board[0][2]),
            },
            {
                "ident": "   TicTacToe   ",
                "col1": center1.format(self.board[1][0]),
                "col2": center2.format(self.board[1][1]),
                "col3": center3.format(self.board[1][2]),
            },
            {
                "ident": "",
                "col1": center1.format(self.board[2][0]),
                "col2": center2.format(self.board[2][1]),
                "col3": center3.format(self.board[2][2]),
            },
        ]

        return TablePrinter(fmt1, ul="")(data1) + "\n"


class RunGame(TicTacToe):
    """Class to run the TicTacToe game"""

    def run(self):
        game = TicTacToe()
        while True:
            print(f"{game.turn_now} turn: ")
            x, y = input("type the cell you want with format i j: ").split(" ")
            status = game.do_the_play(int(x), int(y))
            if status != 0:
                continue
            print(game)
            winner = game.check_for_winner()
            if winner is not None:
                if winner != "tie":
                    print(f"The winner is the {winner}")
                elif winner == "tie":
                    print("The game tied")
                continue_ = input("Continue playing? (N,y)")
                if not continue_:
                    break
                game.new_game()


if __name__ == "__main__":
    # game = TicTacToe()
    # game.do_the_play(1, 1)
    # game.do_the_play(0, 2)
    # game.do_the_play(1, 2)
    # game.do_the_play(1, 0)
    # game.do_the_play(0, 1)
    # game.do_the_play(2, 1)
    # game.do_the_play(2, 2)
    # game.do_the_play(0, 0)
    # print(game)
    # print(game.check_for_winner())

    game = RunGame()
    game.run()
