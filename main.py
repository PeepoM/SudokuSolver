from model import Model
from view import View
from controller import Controller


class Main:
    def __init__(self):
        self.model = Model()
        self.view = View()
        self.controller = Controller(self.model, self.view)

    def main(self):
        self.controller.start_program()


if __name__ == "__main__":
    Main().main()
