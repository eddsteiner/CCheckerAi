#from sys import ps1
import numpy as np
import numpy.typing as npt
import random

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

    def __init__(self) -> None:
        self.move_map = self.get_move_map().astype(np.int32)
        # self.p1 = Creature1
        # self.p2 = Creature2

    #needs to return 1 or 0. 1 means p1 wins 0 means p2 wins
    def run_game(self, p1: Creature, p2: Creature) -> tuple[bool, Stats]:
        """Will run a game on the two provided creatures"""
        #self.p1 = p1
        #self.p2 = p2
        game = ChineseCheckersEngine(p1, p2)

        board1pointer = game.board1.ctypes.data
        board2pointer = game.board2.ctypes.data

        output_buffer_array = np.random.randint(1,418, size = 417)
        #print(output_buffer_array)
        #output_buffer_array = np.empty(417, dtype = np.float32)
        output_buffer = output_buffer_array.ctypes.data
        buffer_rankings = np.zeros(len(output_buffer_array))

        index_count = 0
        start_pos = 0
        action = 0
        move_to_grab = 1

        player = p1 if game.current_player else p2
        board_pointer = board1pointer if game.current_player else board2pointer
        #print(output_buffer)
        
        player.calculate(board_pointer, output_buffer)
        #rank the buffer readings
        sorted_indices = np.argsort(output_buffer_array)[::-1]
        buffer_rankings[sorted_indices] = np.arange(1, len(sorted_indices) + 1)
        print(buffer_rankings)







        #------------------------BROKEN
        #extract startpos and action
        for index in buffer_rankings:
            if index == move_to_grab:
                start_pos = self.move_map[index_count][0]
                action = self.move_map[index_count][1]
                index_count = 0
            else:
                index_count += 1
        
        #insert start pos and action into make_move
        action_result = game.make_move(start_pos, action, p1)
        #while make_move returns -1
        while action_result == -1:
            move_to_grab += 1           #get the next best move
            for index in buffer_rankings:   #look for the next best ranking
                if index == move_to_grab:   #if we find it
                    start_pos = self.move_map[index_count][0] #extract start pos and action
                    action = self.move_map[index_count][1]
                    index_count = 0
                else:
                    index_count += 1
            action_result = game.make_move(start_pos, action, p1) #check to see if it will go -1
        
        if action_result == 2:
            return (True, Stats())
        if action_result == 3:
            return(False, Stats())



            
        

        
        
        
        
        
        return (random.choice([True, False]), Stats())


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
                    # print("tuple ", added_tuple, " added")
                # else:
                    # print("move invalid")
        
        skip_tuples = (skip, moveset[0])                            #add extra move for skipping
        move_map = np.append(move_map, [skip_tuples], axis = 0)     #appends the skip tuple
        print("skip tuple added")


        return move_map


