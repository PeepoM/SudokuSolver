import random as rnd

NR_ROWS = 9
NR_COLS = 9

nr_sols = 0


def solve(board, counting_sols):
    global nr_sols

    position = find_empty_cell(board)

    # If no empty cell was found, we have a solution
    if position is None:
        return True

    row, col = position

    for number in range(1, 10):
        # Check if the number is valid in the spot
        is_valid = is_placement_valid(number, row, col, board)

        # If the spot is valid recursively call solve with a new board, reset the spot otherwise
        if is_valid:
            # Place the number
            board[row][col] = number

            # Return true if we managed to find a solution
            solved = solve(board, counting_sols)
            if solved:
                # If we are counting solutions increment number of solutions, return true otherwise
                if counting_sols:
                    nr_sols += 1
                else:
                    return True

            # If we did not find a solution erase the placed number
            board[row][col] = 0

    return False


def is_placement_valid(num_placed, row_placed, col_placed, board):
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


def find_empty_cell(board):
    for row in range(NR_ROWS):
        for col in range(NR_COLS):
            number = board[row][col]

            # Check if the cell is empty
            if number == 0:
                return row, col


def display_board(board):
    for row in range(NR_ROWS):
        if row % 3 == 0 and row != 0:
            print("---------------------")

        for col in range(NR_COLS):
            number = board[row][col]

            if col % 3 == 0 and col != 0:
                print("| ", end="")

            if col == NR_COLS - 1:
                if number == 0:
                    print(" ")
                else:
                    print(number)
            else:
                if number == 0:
                    print(" ", end=" ")
                else:
                    print(number, end=" ")


def deep_copy(board):
    return [row[:] for row in board]


def empty_board():
    # Generate an empty board
    return [[0 for _ in range(NR_COLS)] for _ in range(NR_ROWS)]


def generate_solution(board):
    position = find_empty_cell(board)

    # If no empty cell was found, we have a solution
    if position is None:
        return True

    row, col = position

    # Generate and shuffle a list of numbers we will be placing on our board
    numbers = list(range(1, 10))
    rnd.shuffle(numbers)

    for number in numbers:
        # Try placing numbers one by one and check if the placement is valid
        is_valid = is_placement_valid(number, row, col, board)

        if is_valid:
            # Place the number onto the board
            board[row][col] = number
            # Recursively generate the final board
            final_board = generate_solution(board)

            # If we managed to fill up the board, return true
            if final_board is not None:
                return True

            # Reset the position and try placing other numbers otherwise
            board[row][col] = 0


def get_non_empty_squares(board):
    non_empty_squares = []

    for row in range(NR_ROWS):
        for col in range(NR_COLS):
            number = board[row][col]
            if number != 0:
                non_empty_squares.append((row, col))

    return non_empty_squares


def remove_numbers(board):
    # Get the non-empty squares and count them
    non_empty_squares = get_non_empty_squares(board)
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

    global nr_sols
    nr_sols = 0

    # Solve the copy of our original board, while counting num. of solutions
    board_copy = deep_copy(board)
    solve(board_copy, True)

    # If num. of solutions is one recursively remove other numbers
    # Otherwise put the removed number back and recursively remove other numbers
    if nr_sols == 1:
        remove_numbers(board)
    else:
        board[row][col] = number
        remove_numbers(board)


# Generate an empty sudoku board
sudoku_board = empty_board()

# Generate a solution to a sudoku
generate_solution(sudoku_board)

print("\nGenerated sudoku solution:")
display_board(sudoku_board)

# Remove numbers but making sure it has only one solution
remove_numbers(sudoku_board)

print("\nSudoku puzzle with removed numbers:")
display_board(sudoku_board)

print("\nSolving the puzzle with backtracking algorithm:")
solve(sudoku_board, False)

display_board(sudoku_board)
