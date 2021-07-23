class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def start_program(self):
        sudoku_board = self.model.board

        self.model.generate_puzzle(sudoku_board)

        print("\nGenerated sudoku puzzle:")
        self.view.display_board(sudoku_board)

        self.model.remove_numbers(sudoku_board)

        print("\nSudoku puzzle with removed numbers:")
        self.view.display_board(sudoku_board)

        self.model.solve(sudoku_board, False)

        print("\nSolving the puzzle with backtracking algorithm:")
        self.view.display_board(sudoku_board)
