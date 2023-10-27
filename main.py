from src.engine import ChineseCheckersEngine

def main():
    
    game = ChineseCheckersEngine()
    game.initialize_board()
    game.print_board()


    game.board1 = list(range(81))
    game.print_board()


if __name__ == "__main__":
    main()
