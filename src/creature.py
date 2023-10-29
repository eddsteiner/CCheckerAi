import numpy as np
import numpy.typing as npt
#from typing import Any, Self

class Creature:
    """An individual capable of playing Chinese Checkers."""

    #genes: 
    #neuralnet: 


    def calculate(self, board: npt.NDArray[np.int32]) -> npt.NDArray[np.int32]:
        """TODO Calculates the Creature's next move based on the board."""
        ret = np.zeros(487, dtype = np.int32) #487 possible moves, 6 for each tile + 1 for not moving
        return ret


def from_genome() -> Creature:
    """TODO Creates a Creature from a genome."""
    return Creature()

def new_creature() -> Creature:
    """TODO Creates a new randomized Creature."""
    return Creature()


