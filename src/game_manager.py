#from sys import ps1
import numpy as np
import numpy.typing as npt

from neat import Creature
from engine import ChineseCheckersEngine

class Stats:
    """Contains stats about a Chinese Checkers game."""
    pass


"""Runs games on two Creatures"""
class GameManager:
    # p1: Creature
    # p2: Creature
    # move_map = self.get_move_map()

    def __init__(self, Creature1, Creature2):
        self.move_map = self.get_move_map().astype(np.int32)
        self.p1 = Creature1
        self.p2 = Creature2


    def run_game(self, p1: Creature, p2: Creature) -> tuple[bool, Stats]:
        """Will run a game on the two provided creatures"""
        #self.p1 = p1
        #self.p2 = p2
        game = ChineseCheckersEngine(p1, p2)
        
        
        
        
        

        return (True, Stats())


    #maps every possible move to an index in an array tuple(start_pos, action). Tile 0 is where move 0 starts
    def get_move_map(self):
        player1 = 0
        player2 = 0
        skip = -1   #value of start_pos when skipping a jump
        game = ChineseCheckersEngine(player1, player2)  #using engine for validating moves
        empty_board = np.zeros(81)  #using to iterate through board
        moveset = [-1, -9, 8, -8, 9, 1] #our llist of possible directions you can move
        move_map = np.empty((0,2), dtype = int) #going to fill this with tuples

        for index in range(len(empty_board)): #going through index 0-80
            for move in moveset:               #going through every move in the moveset array
                if game.is_valid_move(empty_board, index, move):    #if the move is valid
                    added_tuple = (index, move)                     #add the move to the tuple (start_pos, action)
                    move_map = np.append(move_map, [added_tuple], axis=0)   #append that tuple to the move_map
                    print("tuple ", added_tuple, " added")
                else:
                    print("move invalid")
        
        skip_tuples = (skip, moveset[0])                            #add extra move for skipping
        move_map = np.append(move_map, [skip_tuples], axis = 0)     #appends the skip tuple
        print("skip tuple added")


        return move_map


