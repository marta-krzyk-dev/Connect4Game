# "Connect 4" console game

from enum import Enum
from datetime import datetime
from termcolor import colored  # To install termcolor, run "pip install termcolor" in terminal


class Player(Enum):
    RED = 1
    BLACK = 2


# Game class
class Game:
    def __init__(self, column_count, row_count):

        if row_count < 2 or column_count < 2:
            raise ValueError('Row and column count not integers greater than 1')
            return

        self.black_symbol = colored('\u2B24', 'white', attrs=['reverse'])
        self.red_symbol = colored('\u2B24', 'red')
        self.empty_symbol = '  '
        self.connect = 4 # Number of symbol sequence to win the game
        self.min_moves_to_win = (2 * self.connect) - 1
        self.moves_done = 0
        self.empty_spots = column_count * row_count
        self.column_count = column_count
        self.row_count = row_count
        self.last_drop_row = None
        self.last_drop_col = None
        # Initialize board with empty spots
        self.board = [[self.empty_symbol for r in range(column_count)]
                      for c in range(row_count)]

    def DrawBoard(self):

        row_dashes = "-" * ((self.column_count * 3) - 1)
        horizontal_border_bar = "*" + row_dashes + "*"
        col_num_bar = "| " + "| ".join(str(i) for i in range(1, self.column_count + 1)) + "|"

        print(col_num_bar, end="\n")
        print(horizontal_border_bar)
        i = 1
        for row in self.board:
            print("|", end="")

            for col in row:
                print(f"{col}|", end="")

            if i < row_count:
                print("\n*" + row_dashes + "*")
            i += 1

        print("\n" + horizontal_border_bar, end="\n")
        print(col_num_bar)

    def IsBoardFull(self):
        return self.empty_spots == 0

    def ChooseColumn(self, player):
        while True:
            if (player is Player.BLACK):
                column_num = input(
                    colored(f"{player} choose column(1-{self.column_count}):", 'white', attrs=['reverse', 'bold']))
            else:
                column_num = input(
                    colored(f"{player} choose column(1-{self.column_count}):", 'grey', 'on_red', attrs=['bold']))

            column_num = tryConvertToInt(column_num)

            if column_num is False or column_num < 1 or column_num > self.column_count:
                print("Invalid column number. Try again.")
            elif self.board[0][column_num - 1] is not self.empty_symbol:
                print("Column is full. Choose another one.")
            else:
                return column_num

    def DropElement(self, column_num, player):

        column_num -= 1  # Convert to index_based number

        if column_num < 0 or column_num >= self.column_count:
            return False

        for row_num in reversed(range(self.row_count)):  # [5,4,3,2,1,0]
            if self.board[row_num][column_num] is self.empty_symbol:
                self.board[row_num][column_num] = self.red_symbol if player is Player.RED else self.black_symbol
                self.empty_spots -= 1
                self.moves_done += 1
                self.last_drop_row = row_num # Save the position of the last drop for CheckWin()
                self.last_drop_col = column_num
                return True

        return False

    def CheckWin(self):

        if self.moves_done < self.min_moves_to_win:
            return False

        symbol = self.board[self.last_drop_row][self.last_drop_col]

        return self.CheckWinHorizontally(symbol) or self.CheckWinVertically(symbol) or self.CheckWinDiagonally(
            symbol, -1) or self.CheckWinDiagonally(symbol)

    def CheckWinHorizontally(self, symbol):

        # take up 0-3 elements ahead and after the last dropped element
        row = self.board[self.last_drop_row]
        to_take = self.connect - 1
        before = self.last_drop_col - to_take
        before = 0 if before < 0 else before
        after = self.last_drop_col + self.connect
        after = self.column_count - 1 if after >= self.column_count else after

        search_string = ''.join(row[before:after])  # Put all elements into a string, eg. "⬤  ⬤⬤  "
        win_string = symbol * self.connect

        return win_string in search_string

        # eg. "⬤⬤⬤⬤" in "  ⬤⬤⬤⬤   ⬤" is a win
        # eg. "⬤⬤⬤⬤" in "⬤  ⬤⬤  " is a lose

    def CheckWinVertically(self, symbol):

        # take up 0-3 elements above and below the last dropped element
        to_take = self.connect - 1
        above = 0 if (self.last_drop_row - to_take) < 0 else (self.last_drop_row - to_take)

        below = self.last_drop_row + self.connect
        below = self.row_count - 1 if below > self.row_count else below

        full_column = [r[self.last_drop_col] for r in self.board]
        search_string = ''.join(full_column[above:below])
        win_string = symbol * self.connect

        return win_string in search_string

    # If direction == 1 check diagonal from top left to bottom right
    # If direction == -1 check diagonal from top right to bottom left
    def CheckWinDiagonally(self, symbol, direction=1):

        search_string = symbol
        win_string = symbol * self.connect

        row_below = self.last_drop_row + 1
        col_below = self.last_drop_col + 1 * direction

        while self.IndexesAreCorrect(row_below, col_below):
            if self.board[row_below][col_below] is symbol:
                search_string = symbol + search_string
                if win_string in search_string:
                    return True
                row_below += 1
                col_below += 1 * direction
            else:
                break # If the next neighbour is not the same symbol, look no futher

        row_above = self.last_drop_row - 1
        col_above = self.last_drop_col - 1 * direction

        while self.IndexesAreCorrect(row_above, col_above):
            if self.board[row_above][col_above] is symbol:
                search_string += symbol
                if win_string in search_string:
                    return True
                row_above -= 1
                col_above -= 1 * direction
            else:
                break

        return win_string in search_string

    def IndexesAreCorrect(self, row_below, col_below):
        return row_below >= 0 and row_below < self.row_count and col_below >= 0 and col_below < self.column_count


# Helper methods
def tryConvertToInt(value):
    try:
        return int(value)  # If conversion is a success, return the integer
    except ValueError:
        return False


# Main program
second_is_even = datetime.today().second % 2 == 0
player = Player.RED if second_is_even else Player.BLACK  # Choose "random" player to start

column_count = 7
row_count = 6

game = Game(column_count, row_count)

while True:
    game.DrawBoard()

    column_num = game.ChooseColumn(player)
    game.DropElement(column_num, player)

    if game.CheckWin():
        game.DrawBoard()
        if (player is Player.BLACK):
            print(colored(f"{str(player)} won!", 'white', attrs=['reverse', 'bold']))
        else:
            print(colored(f"{str(player)} won!", 'grey', 'on_red', attrs=['bold']))
        input(colored("Click enter to start another game!", 'magenta', attrs=['reverse', 'bold']))
        game = Game(column_count, row_count)

    if game.IsBoardFull():
        game.DrawBoard()
        print(colored("The board is full. No winner.", 'magenta', attrs=['reverse', 'bold']))
        input(colored("Click enter to start another game!", 'magenta', attrs=['reverse', 'bold']))
        game = Game(column_count, row_count)

    # Change player (another turn)
    player = Player.RED if player == Player.BLACK else Player.BLACK
