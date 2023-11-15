import numpy as np

from engine import ChineseCheckersEngine


def main():
    
    game = ChineseCheckersEngine(None, None)
    game.initialize_board()
    
    #menu
    PlayerChoice = input('Choose an option: 1. Play 2. Exit')
    PlayerChoice = int(PlayerChoice)

    while (PlayerChoice == 1):
        #Player 1 turn
        print('---------------------------')
        print('---------------------------')
        print('---------------------------')
        print('PLAYER 1 TURN')
        game.print_board()
        p1_start_pos = input('Pick starting piece')
        p1_start_pos = int(p1_start_pos)
        p1_action = input('pick action')
        p1_action = int(p1_action)
 
        while not game.update_board(p1_start_pos, p1_action):
            p1_start_pos = input('Pick new starting piece')
            p1_start_pos = int(p1_start_pos)
            p1_action = input('pick new action')
            p1_action = int(p1_action)

        #switch player
        game.switch_player()
        #player 2 turn
        print('---------------------------')
        print('---------------------------')
        print('---------------------------')
        print("PLAYER 2 TURN")
        game.print_board()
        p2_start_pos = input('Pick starting piece')
        p2_start_pos = int(p2_start_pos)
        p2_action = input('pick action')
        p2_action = int(p2_action)
 
        while not game.update_board(p2_start_pos, p2_action):
            p2_start_pos = input('Pick new starting piece')
            p2_start_pos = int(p2_start_pos)
            p2_action = input('pick new action')
            p2_action = int(p2_action)
        game.switch_player()
        game.print_board()
        PlayerChoice = input('keep Playing? 1. yes 2. no')
        PlayerChoice = int(PlayerChoice)
        








    #game.print_board()


    #game.board1 = np.array(list(range(81)))
    #game.print_board()


if __name__ == "__main__":
    main()

