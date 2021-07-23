from model import Model


class View:
    def display_board(self, board):
        for row in range(Model.NR_ROWS):
            if row % 3 == 0 and row != 0:
                print("---------------------")

            for col in range(Model.NR_COLS):
                number = board[row][col]

                if col % 3 == 0 and col != 0:
                    print("| ", end="")

                if col == Model.NR_COLS - 1:
                    if number == 0:
                        print(" ")
                    else:
                        print(number)
                else:
                    if number == 0:
                        print(" ", end=" ")
                    else:
                        print(number, end=" ")
