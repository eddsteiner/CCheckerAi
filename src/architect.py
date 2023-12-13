from multiprocessing.context import Process
import numpy as np
import numpy.typing as npt
import random
import multiprocessing

from neat import GenerationManager, Creature
from game_manager import GameManager, Stats


GENERATION_SIZE = 500
THREAD_COUNT = 25

if (GENERATION_SIZE % THREAD_COUNT) != 0:
    raise Exception("bad thread count")
THREAD_SIZE = int(GENERATION_SIZE / THREAD_COUNT)


class BigStats:
    """Contains statistics about a generation"""
    average_center_entropy: float
    average_turns: float
    average_nodes: float
    average_connections: float


class Architect:
    """Manages and evolves generations of Creatures."""


    def __init__(self):
        self.neat = GenerationManager(GENERATION_SIZE, 81, 417) 
        self.stats: list[BigStats] = []


    def evolve(self) -> bool:
        """
        Plays through one generation of evolution.

        Returns True if process succeeded, False otherwise.
        """

        print("evolving one generation")
        return self.__evolution(self.__ranking())


    def __handle_creature(self, thread_id: int, all_creatures: list[Creature], gen: int):
        """Play 10 games for a given creature."""
        game = GameManager()
        for creature_index in range(THREAD_SIZE): #playing x creatures
            for _ in range(10):  #playing 10 games per creature

                creature2_index = random.randint(0, GENERATION_SIZE-1)
                while creature2_index == creature_index: #don't play a creature against itself
                    creature2_index = random.randint(0, GENERATION_SIZE-1)

                #print(creature2_index, len(all_creatures))
                creature1 = all_creatures[creature_index + thread_id]
                creature2 = all_creatures[creature2_index]
                result, stats = game.run_game(creature1, creature2)    #run the game with the creatures
                #if result:  #if creature 1 wins: add 1 to the creature 1 index in the wins array
                    #wins_array[creature_index + thread_id] += 1

                text = f"turns: {stats.turns}\n"
                text += f"nodes: {stats.player1_nodes}\n"
                text += f"connections: {stats.player1_connections}\n"
                text += f"entropy: {stats.player1_spread}\n"
                with open(f"output/gen_{gen}_cr_{thread_id + creature_index}.stats", "w") as file:
                    file.write(text)



    def __ranking(self) -> npt.NDArray[np.int32]:
        """
        TODO Runs a tournament for the whole generation.

        Returns rankings as a numpy array.
        """

        #do all the tournament things here
        
        rankings = np.array(range(GENERATION_SIZE), dtype = np.int32)
        wins_array = np.zeros(len(rankings), dtype = np.int32) #update this with wins
        all_creatures = self.neat.get_current_generation()
        gen_stats: list[Stats] = []
        threads: list[Process] = [Process()]*GENERATION_SIZE

        for i in range(0, GENERATION_SIZE, THREAD_SIZE):  #loops through all creatures to feed to thread
            threads[i] = multiprocessing.Process(target = self.__handle_creature, args = (i, all_creatures, 0))
        for i in range(0, GENERATION_SIZE, THREAD_SIZE):  #initialize all threads
            threads[i].start()
        for i in range(0, GENERATION_SIZE, THREAD_SIZE):  #collect all threads
            threads[i].join()
            print(f"joined thread {i}")
        
        # Sort the creatures based on wins and update the rankings array
        sorted_indices = np.argsort(wins_array)[::-1]
        rankings[sorted_indices] = np.arange(1, len(sorted_indices) + 1)
        #print("\n\n\nrankings array")
        #print(rankings)
        #print("wins array")
        #print(wins_array)
        
        # process stats
        total_turns = 0
        total_nodes = 0
        total_connections = 0
        total_entropy = 0.0
        for stat in gen_stats:
            total_turns += stat.turns
            total_nodes += stat.player1_nodes
            total_connections += stat.player1_connections
            total_entropy += stat.player1_spread
        bigstats = BigStats()
        print(len(gen_stats))
        bigstats.average_turns = total_turns / len(gen_stats)
        bigstats.average_nodes = total_nodes / len(gen_stats)
        bigstats.average_connections = total_connections / len(gen_stats)
        bigstats.average_center_entropy = total_entropy / len(gen_stats)

        self.stats.append(bigstats)

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




