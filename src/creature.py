import numpy as np
import numpy.typing as npt
from typing import Any


class Creature:
    """An individual capable of playing Chinese Checkers."""

    def __init__(self, genome: Any):
        #make sure to specify the genome's type once we figure that out
        #don't add a default parameter to reduce chances of mistakes later
        self.generate_neuralnet()
        pass


    def generate_neuralnet(self):
        """TODO Reads the genome and generates a neural network."""
        pass


    def calculate(self, board: npt.NDArray[np.int32]) -> npt.NDArray[np.int32]:
        """TODO Calculates the Creature's next move based on the board."""
        ret = np.zeros(487, dtype = np.int32) #487 possible moves, 6 for each tile + 1 for not moving
        return ret


def from_genome(genome: Any) -> Creature:
    """TODO Creates a Creature from a genome."""
    #will set the creature's neural network and call generate_neuralnet()
    #remember to set genome's type later
    return Creature(genome)


def random_creature() -> Creature:
    """TODO Creates a new randomized Creature."""
    #generate a random genome here and then feed it to the creature
    genome = None
    return Creature(genome)


