import copy
import random as rnd


class Model:
    NR_ROWS = 9
    NR_COLS = 9

    def __init__(self):
        self._nr_sols = 0

        self.board = self.empty_board()

    def solve(self, board, counting_sols):
        position = self.find_empty_cell(board)

        # If no empty cell was found, we have a solution
        if position is None:
            return True

        row, col = position

        for number in range(1, 10):
            # Check if the number is valid in the spot
            is_valid = self.is_placement_valid(number, row, col, board)

            # If the spot is valid recursively call solve with a new board, reset the spot otherwise
            if is_valid:
                # Place the number
                board[row][col] = number

                # Return true if we managed to find a solution
                solved = self.solve(board, counting_sols)
                if solved:
                    # If we are counting solutions increment number of solutions, return true otherwise
                    if counting_sols:
                        self._nr_sols += 1
                    else:
                        return True

                # If we did not find a solution erase the placed number
                board[row][col] = 0

        return False

    def is_placement_valid(self, num_placed, row_placed, col_placed, board):
        # Check rows
        for number in board[row_placed]:
            if number == num_placed:
                return False

        # Check columns
        for row in board:
            number = row[col_placed]
            if number == num_placed:
                return False

        # Check all 3 x 3 squares
        box_row_start = row_placed // 3
        box_col_start = col_placed // 3

        for row in range(box_row_start * 3, box_row_start * 3 + 3):
            for col in range(box_col_start * 3, box_col_start * 3 + 3):
                number = board[row][col]
                if number == num_placed and (row != row_placed
                                             or col != col_placed):
                    return False

        return True

    def find_empty_cell(self, board):
        for row in range(Model.NR_ROWS):
            for col in range(Model.NR_COLS):
                number = board[row][col]

                # Check if the cell is empty
                if number == 0:
                    return row, col

    def empty_board(self):
        # Generate an empty board
        return [[0 for _ in range(Model.NR_COLS)]
                for _ in range(Model.NR_ROWS)]

    def generate_puzzle(self, board):
        position = self.find_empty_cell(board)

        # If no empty cell was found, we have a solution
        if position is None:
            return True

        row, col = position

        # Generate and shuffle a list of numbers we will be placing on our board
        numbers = list(range(1, 10))
        rnd.shuffle(numbers)

        for number in numbers:
            # Try placing numbers one by one and check if the placement is valid
            is_valid = self.is_placement_valid(number, row, col, board)

            if is_valid:
                # Place the number onto the board
                board[row][col] = number
                # Recursively generate the final board
                final_board = self.generate_puzzle(board)

                # If we managed to fill up the board, return true
                if final_board is not None:
                    return True

                # Reset the position and try placing other numbers otherwise
                board[row][col] = 0

    def get_non_empty_squares(self, board):
        non_empty_squares = []

        for row in range(Model.NR_ROWS):
            for col in range(Model.NR_COLS):
                number = board[row][col]
                if number != 0:
                    non_empty_squares.append((row, col))

        return non_empty_squares

    def remove_numbers(self, board):
        # Get the non-empty squares and count them
        non_empty_squares = self.get_non_empty_squares(board)
        num_of_non_empty_squares = len(non_empty_squares)

        # Return board if the number of filled squares is 30
        if num_of_non_empty_squares <= 30:
            return board

        # Shuffle the list of squares to make the removal random
        rnd.shuffle(non_empty_squares)

        row, col = non_empty_squares.pop()

        # Store the number before removal and then remove it
        number = board[row][col]
        board[row][col] = 0

        self._nr_sols = 0

        # Solve the copy of our original board, while counting num. of solutions
        board_copy = copy.deepcopy(board)
        self.solve(board_copy, True)

        # If num. of solutions is one recursively remove other numbers
        # Otherwise put the removed number back and recursively remove other numbers
        if self._nr_sols == 1:
            self.remove_numbers(board)
        else:
            board[row][col] = number
            self.remove_numbers(board)
