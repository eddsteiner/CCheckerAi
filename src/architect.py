import numpy as np
import numpy.typing as npt
import random

from neat import GenerationManager, Creature
from game_manager import GameManager, Stats


GENERATION_SIZE = 500


class Architect:
    """Manages and evolves generations of Creatures."""


    def __init__(self):
        self.neat = GenerationManager(GENERATION_SIZE, 81, 417) 
        self.stats: list[Stats] = []


    def evolve(self) -> bool:
        """
        Plays through one generation of evolution.

        Returns True if process succeeded, False otherwise.
        """

        print("evolving one generation")
        return self.__evolution(self.__ranking())


    def __ranking(self) -> npt.NDArray[np.int32]:
        """
        TODO Runs a tournament for the whole generation.

        Returns rankings as a numpy array.
        """

        #do all the tournament things here
        
        game = GameManager()
        rankings = np.array(range(GENERATION_SIZE), dtype = np.int32)
        wins_array = np.zeros(len(rankings), dtype = np.int32) #update this with wins
        all_creatures = self.neat.get_current_generation()

        for i in range(len(all_creatures)):  #loops through all creatures to feed to game manager
            #print(f"running games for creature {i}")
            creature = all_creatures[i]
            
            for j in range(10):  #playing 10 games per creature
                #print(f"running game {j}")
                creature1 = creature
                creature2 = all_creatures[random.randint(0, len(all_creatures) - 1)]  #randomizing creature 2

                while creature2 == creature1:   #keeps looking for new creature if creature 1 and 2 are the same
                    creature2 = all_creatures[random.randint(0, len(all_creatures) - 1)]
                
                #print(f"before")
                result, stats = game.run_game(creature1, creature2)    #run the game with the creatures
                self.stats.append(stats)
                #print(f"after")
                if result:  #if creature 1 wins: add 1 to the creature 1 index in the wins array
                    wins_array[i] += 1
        
        # Sort the creatures based on wins and update the rankings array
        sorted_indices = np.argsort(wins_array)[::-1]
        rankings[sorted_indices] = np.arange(1, len(sorted_indices) + 1)
        #print("\n\n\nrankings array")
        #print(rankings)
        #print("wins array")
        #print(wins_array)

        return rankings


    def __evolution(self, rankings: npt.NDArray[np.int32]) -> bool:
        """
        Calls NEAT's evolve function, enacting the rankings and repopulation.

        Returns True if process succeeded, False otherwise.
        """

        #want to call the internal deallocation function, as well as the internal repopulate function
        #just do a bunch of internal things and then call them here, while considering memory safety
        #rankings = self.__ranking()
        
        return self.neat.evolve(rankings.ctypes.data)




