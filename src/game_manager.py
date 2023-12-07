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



    def get_move_map(self):
        player1 = 0
        player2 = 0
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


        return move_map


