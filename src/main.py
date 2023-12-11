from multiprocessing import Array
import numpy as np
import random

from engine import ChineseCheckersEngine
from architect import Architect
from game_manager import GameManager


#fail cases 79 + 1, 9 - 9 (gives 89 do to the opposite side), something wrong with corner (71, 79, 80) 
#need to fix 79 and fix other similar cases (and figure out what makes these cases special.)


def main():
    p1 = 0
    p2 = 0
    manager = GameManager(p1, p2)
    #array = manager.get_move_map()
    print(manager.move_map)
    length = len(manager.move_map)
    dtype_of_move_map = manager.move_map.dtype  # Get the dtype of the array
    print("dtype: ", dtype_of_move_map)
    print("array length: ", length)
    
    
    
    
    
    
    
    
    
    
    # test = Architect()
    # rankingsArray = test.evolve()
    # print(rankingsArray)





    # game = ChineseCheckersEngine(None, None)
    # game.initialize_board()
    # game.board1 = np.array(list(range(81)))
    # game.print_board()
    #print("hello")
    #menu
    # PlayerChoice = input('Choose an option: 1. Play 2. Exit')
    # PlayerChoice = int(PlayerChoice)
    # moves = [-1, -9, 8, -8, 9, 1]
    # my_array = list(range(81))
    # random_startpos = random.choice(my_array)
    # random_action = random.choice(moves)
    # game.switch_player()




#     while (PlayerChoice == 1):
#         #Player 1 turn
#         print('---------------------------')
#         print('---------------------------')
#         print('---------------------------')
#         print('PLAYER 1 TURN')
#         game.print_board()
#         p1_start_pos = input('Pick starting piece')
#         p1_start_pos = int(p1_start_pos)
#         p1_action = input('pick action')
#         p1_action = int(p1_action)
 
#         while not game.update_board(p1_start_pos, p1_action):
#             p1_start_pos = input('Pick new starting piece')
#             p1_start_pos = int(p1_start_pos)
#             p1_action = input('pick new action')
#             p1_action = int(p1_action)

#         #switch player
#         game.switch_player()
#         #player 2 turn
#         print('---------------------------')
#         print('---------------------------')
#         print('---------------------------')
#         print("PLAYER 2 TURN")
#         game.print_board()


#         #for user play---------------------------
#         p2_start_pos = input('Pick starting piece')
#         p2_start_pos = int(p2_start_pos)
#         p2_action = input('pick action')
#         p2_action = int(p2_action)
#         #------------------------------------------


#         #random number testing------------------------------------
#         # random_startpos = random.choice(my_array)
#         # random_action = random.choice(moves)
#         # print("new ", random_startpos, " ---- ", random_action)
#         #---------------------------------------------------------


#         while not game.update_board(p2_start_pos, p2_action):
#             #random number -------------------------------------------------------------------------
#             # print("!!!!! start = ", random_startpos, " !!!!!! action = ", random_action)
#             # print("picking a new start and action...")
#             # print("!!!!!!!!")
#             # random_startpos = random.choice(my_array)
#             # random_action = random.choice(moves)
#             # print("new ", random_startpos, " ---- ", random_action)
#             #---------------------------------------------------------------------------------


#             #user-------------------------------------------------
#             p2_start_pos = input('Pick new starting piece')
#             p2_start_pos = int(p2_start_pos)
#             p2_action = input('pick new action')
#             p2_action = int(p2_action)
#             # #--------------------------------------------------



#         #game.switch_player()
#         game.print_board()
#         PlayerChoice = input('keep Playing? 1. yes 2. no')
#         PlayerChoice = int(PlayerChoice)
        








#     #game.print_board()


#     #game.board1 = np.array(list(range(81)))
#     #game.print_board()


if __name__ == "__main__":
    main()

