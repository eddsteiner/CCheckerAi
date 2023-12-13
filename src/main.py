from multiprocessing import Array
import numpy as np
import random

from engine import ChineseCheckersEngine
from architect import Architect
from game_manager import GameManager


#fail cases 79 + 1, 9 - 9 (gives 89 do to the opposite side), something wrong with corner (71, 79, 80) 
#need to fix 79 and fix other similar cases (and figure out what makes these cases special.)


def main():
    # p1 = 0
    # p2 = 0
    # manager = GameManager(p1, p2)
    # #array = manager.get_move_map()
    # print(manager.move_map)
    # length = len(manager.move_map)
    # dtype_of_move_map = manager.move_map.dtype  # Get the dtype of the array
    # print("dtype: ", dtype_of_move_map)
    # print("array length: ", length)
    
    
    
    
    
    
    #win test
    # game = ChineseCheckersEngine(p1, p2)
    # winarray = np.ones(81)
    # notwin = np.zeros(81)
    # game.board2 = notwin
    # print(game.check_win())
    #print(game.check_win(notwin))
    
    print("going to initialize")
    model = Architect()
    print("initialized")
    #rankingsArray = test.evolve()
    #print(rankingsArray)

    for i in range(1): #train for x generations
        model.evolve()





if __name__ == "__main__":
    main()

