import numpy as np

from engine import ChineseCheckersEngine


def main():
    
    game = ChineseCheckersEngine(None, None)
    game.initialize_board()
    game.print_board()


    game.board1 = np.array(list(range(81)))
    game.print_board()


if __name__ == "__main__":
    main()

