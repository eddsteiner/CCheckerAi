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
    p1: Creature
    p2: Creature
    
    def run_game(self, p1: Creature, p2: Creature) -> tuple[bool, Stats]:
        """Will run a game on the two provided creatures"""
        self.p1 = p1
        self.p2 = p2
        

        return (True, Stats())


    #maps every possible move to an index in an array tuple(start_pos, action). Tile 0 is where move 0 starts
    def get_move_map(self):
        player1 = 0
        player2 = 0
        skip = -1
        game = ChineseCheckersEngine(player1, player2)
        empty_board = np.zeros(81)
        moveset = [-1, -9, 8, -8, 9, 1]
        move_map = np.empty((0,2), dtype = int)

        for index in range(len(empty_board)):
            for move in moveset:
                if game.is_valid_move(empty_board, index, move):
                    added_tuple = (index, move)
                    move_map = np.append(move_map, [added_tuple], axis=0)
                    print("tuple ", added_tuple, " added")
                else:
                    print("move invalid")
        for move in moveset: #adds extra moves containing -1 as the start pos (this means skip)
            skip_tuples = (skip, move)
            move_map = np.append(move_map, [skip_tuples], axis = 0)
            print("skip tuple added")


        return move_map


