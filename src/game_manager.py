import numpy as np
import numpy.typing as npt

from neat import Creature


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




