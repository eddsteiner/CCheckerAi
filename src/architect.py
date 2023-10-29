import numpy as np
import numpy.typing as npt
from typing import Any

from creature import Creature, from_genome, new_creature


GENERATION_SIZE = 500


class Architect:
    """Manages and evolves generations of Creatures."""


    def __init__(self):
        self.generation = np.empty((GENERATION_SIZE), dtype = Creature)
        """Contains all the creatures in this generation."""


    def reproduce(self, parent1: Creature, parent2: Creature) -> Creature:
        """TODO Takes two parents and produces a child."""
        child = from_genome()

        return child


    def save_generation(self, file_name: str):
        """TODO Saves the current sorted generation to a file."""
        pass


    def load_generation(self, file_name: str):
        """TODO Loads a sorted generation from a file."""
        pass






