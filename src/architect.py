import numpy as np
import numpy.typing as npt

from neat import NEAT, Creature


GENERATION_SIZE = 500


class Architect:
    """Manages and evolves generations of Creatures."""


    def __init__(self):
        self.neat = NEAT()
        """Contains all the creatures in this generation."""


    def save_generation(self) -> bool:
        """
        TODO Saves the current sorted generation to a file.

        Returns True if process succeeded, False otherwise.
        """

        # ensure the folder where we save generations is created
        gen = self.neat.generation_number
        ranking = self.__ranking()
        file_name = f"generations/gen_{gen}.gen"
        return self.neat.save_generation(ranking.ctypes.data, file_name) #save


    def load_generation(self, file_name: str) -> bool:
        """
        Loads a sorted generation from a file.

        Returns True if process succeeded, False otherwise.
        """

        return self.neat.load_generation(file_name)


    def evolve(self) -> bool:
        """
        Plays through one generation of evolution.

        Returns True if process succeeded, False otherwise.
        """

        return self.__evolution(self.__ranking())


    def __ranking(self) -> npt.NDArray[np.int32]:
        """
        TODO Runs a tournament for the whole generation.

        Returns rankings as a numpy array.
        """

        rankings = np.zeros(GENERATION_SIZE, dtype = np.int32)

        #do all the tournament things here
        all_creatures = self.neat.get_current_generation()

        return rankings


    def __evolution(self, rankings: npt.NDArray[np.int32]) -> bool:
        """
        Calls NEAT's evolve function, enacting the rankings and repopulation.

        Returns True if process succeeded, False otherwise.
        """

        return self.neat.evolve(rankings.ctypes.data)



