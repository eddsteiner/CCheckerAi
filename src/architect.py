import numpy as np
import numpy.typing as npt
import random

from neat import GenerationManager, Creature
from game_manager import GameManager


GENERATION_SIZE = 500


class Architect:
    """Manages and evolves generations of Creatures."""


    def __init__(self):
        self.neat = GenerationManager(81, 255, GENERATION_SIZE) #THE 255 IS TEMPORARY, CHANGE LATER TODO
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

        #do all the tournament things here
        game = GameManager()
        rankings = np.array(range(GENERATION_SIZE), dtype = np.int32)
        all_creatures = self.neat.get_current_generation()
        rankings = np.zeros(501)
        #all_creatures = np.arange(501)
        wins_array = np.zeros(501) #update this with wins
        print(all_creatures)
        print(wins_array)
        
        for creature in all_creatures:  #loops through all creatures to feed to game manager
            games = 0
            while games <= 9:  #playing 10 games per creature
                creature1 = creature
                creature2 = all_creatures[random.randint(0, len(all_creatures) - 1)]  #randomizing creature 2

                while creature2 == creature1:   #keeps looking for new creature if creature 1 and 2 are the same
                    creature2 = all_creatures[random.randint(0, len(all_creatures) - 1)]
                
                #result = self.testgamemanager()
                result = game.run_game(creature1, creature2)    #run the game with the creatures

                if result:  #if creature 1 wins: add 1 to the creature 1 index in the wins array
                    wins_array[creature1] += 1
                # else:       #if creature 2 wins: add 1 to the creature 2 index in the wins array
                #     wins_array[creature2] += 1

                games += 1 #iterate game


        #print(wins_array)
        # max_wins = int(max(wins_array))
        # wins_array = wins_array.astype(int)

        # while len(wins_array) != len(set(wins_array)):
        #     max_wins = int(max(wins_array))
        #     #print("there are ties")
        #     # Create a list of lists where the index represents the number of wins
        #     win_groups = [[] for _ in range(max_wins + 1)] #if the max is 10 wins, there are 11 empty arrays in the array
        #     for i, wins in enumerate(wins_array): #i is index of element wins is the value of the element: Example [0,1,2,2,1,0] => [[0,5], [1,4] [2,3]]
        #         win_groups[wins].append(i)

        #     # Make all tied creatures play again
        #     for ties in win_groups:
        #         for i in range(len(ties)):
        #             for j in range(i + 1, len(ties)):
        #                 creature1 = all_creatures[ties[i]]
        #                 creature2 = all_creatures[ties[j]]
        #                 result = self.testgamemanager()
        #                 #result = game.run_game(creature1, creature2)

        #                 if result:
        #                     wins_array[ties[i]] += 1
        #                 else:
        #                     wins_array[ties[j]] += 1
        
        # Sort the creatures based on wins and update the rankings array
        sorted_indices = np.argsort(wins_array)[::-1]
        rankings[sorted_indices] = np.arange(1, len(sorted_indices) + 1)
        print("\n\n\nrankings array")
        print(rankings)
        print("wins array")
        print(wins_array)


                


                

        return rankings


    def __evolution(self, rankings: npt.NDArray[np.int32]) -> bool:
        """
        Calls NEAT's evolve function, enacting the rankings and repopulation.

        Returns True if process succeeded, False otherwise.
        """

        #want to call the internal deallocation function, as well as the internal repopulate function
        #just do a bunch of internal things and then call them here, while considering memory safety
        rankings = self.__ranking()
        

        return self.neat.evolve(rankings.ctypes.data)

    def testgamemanager(self):
        return random.choice([True, False])


