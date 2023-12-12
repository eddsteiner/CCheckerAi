import numpy as np
import numpy.typing as npt
import random
from math import e

from neat import Creature
from engine import ChineseCheckersEngine


class Stats:
    """Contains stats about a Chinese Checkers game."""
    turns: int
    tied: bool
    player1_spread: float
    player1_nodes: int
    player1_connections: int
    player2_spread: float
    player2_nodes: int
    player2_connections: int


class GameManager:
    """Runs a game on two Creatures."""
    
    def __init__(self):
        self.tile_map, self.action_map = self.create_move_map()


    """ Tile Numbers

        0  1  2  3  4  5  6  7  8
        9  10 11 12 13 14 15 16 17
        18 19 20 21 22 23 24 25 26
        27 28 29 30 31 32 33 34 35
        36 37 38 39 40 41 42 43 44
        45 46 47 48 49 50 51 52 53
        54 55 56 57 58 59 60 61 62
        63 64 65 66 67 68 69 70 71
        72 73 74 75 76 77 78 79 80
    """


    def map_move(self, num: int) -> tuple[np.int32, np.int32]:
        """Maps a number to its tile and action."""
        return self.tile_map[num], self.action_map[num]


    def entropy(self, lis: npt.NDArray[np.int32]) -> float:
        s = lis.sum()
        if s == 0:
            return 0
        div = lis / lis.sum()
        base = e if div == None else div
        return -(div * np.log(div)/np.log(base)).sum()


    def run_game(self, creature1: Creature, creature2: Creature) -> tuple[bool, Stats]:
        """Runs one game on two creatures."""
        swap_players = random.getrandbits(1) == 1
        if swap_players: #want to randomize who's player1 and player2
            player1 = creature2
            player2 = creature1
        else:
            player1 = creature1
            player2 = creature2

        result = -1
        game = ChineseCheckersEngine()
        output_buffer_array = np.zeros(417, dtype = np.float32)
        output_buffer_pointer = output_buffer_array.ctypes.data
        game_running = True
        last_player = game.current_player

        turn_count = 0
        middle_row1 = np.zeros(9, dtype = np.int32)
        middle_row2 = np.zeros(9, dtype = np.int32)

        while game_running: #unti the game ends
            if last_player != game.current_player:
                if turn_count == 1000: #keep track of how many turns have happened
                    game_running = False
                    break
                else:
                    turn_count += 1
                    last_player = game.current_player

            (player1 if game.current_player else player2).calculate( #grab correct player
                (game.board1 if game.current_player else game.board2).ctypes.data, #grab correct board
                output_buffer_pointer #feed the output buffer
            ) #calculate the move confidences
            sorted_indices = output_buffer_array.argsort()[::-1] #sort max to min
            for i in sorted_indices:
                tile, action = self.map_move(i) #map the next best move
                #print(i, tile, action)
                result = game.make_move(tile, action) #now that we have the move, feed it to the game
                match result:
                    case -1: #move is invalid, try the next one
                        continue
                    case 0: #move is valid, now the other persons's turn
                        if tile in game.middle_row:
                            middle_row = middle_row1 if game.current_player else middle_row2
                            middle_row[game.middle_row_dict[tile]] #count the index in middle row
                        break
                    case 1: #more jumps available, recalculate
                        break
                    case 2: #game was just won by the current player
                        game_running = False
                        break
        
        # record the stats
        stats = Stats()
        stats.turns = turn_count
        stats.player1_nodes = creature1.node_count
        stats.player1_connections = creature1.connection_count
        stats.player2_nodes = creature2.node_count
        stats.player2_connections = creature2.connection_count
        middle1 = middle_row2 if swap_players else middle_row1
        middle2 = middle_row1 if swap_players else middle_row2
        stats.player1_spread = self.entropy(middle1)
        stats.player2_spread = self.entropy(middle2)

        if turn_count == 1000: #game tied, choose random winner
            stats.tied = True
            return (random.getrandbits(1) == 1, Stats())

        stats.tied = False
        return (not game.current_player) if swap_players else game.current_player, Stats()

       
    def create_move_map(self) -> tuple[npt.NDArray[np.int32], npt.NDArray[np.int32]]:
        """Initializes the move map. This function could be very much optimized."""
        tiles = np.zeros(417, dtype = np.int32)
        actions = np.zeros(417, dtype = np.int32)
        offset = 0
        
        # {-1, -9, 8, -8, 9, 1} #upleft, upright, left, right, downleft, downright, NOTE: skips are disallowed normally

        for i in range(81): #for every tile
            mod = i % 9
            if i == 0: #top left
                tiles[offset] = i
                tiles[offset+1] = i
                actions[offset] = 9 #downleft
                actions[offset+1] = 1 #downright
                offset += 2
            elif i == 80: #bottom right
                tiles[offset] = i
                tiles[offset+1] = i
                actions[offset] = -1 #upleft
                actions[offset+1] = -9 #upright
                offset += 2
            elif i == 8: #top right
                tiles[offset] = i
                tiles[offset+1] = i
                tiles[offset+2] = i
                actions[offset] = -1 #upleft
                actions[offset+1] = 8 #left
                actions[offset+2] = 9 #downleft
                offset += 3
            elif i == 72: #bottom left
                tiles[offset] = i
                tiles[offset+1] = i
                tiles[offset+2] = i
                actions[offset] = -9 #upright
                actions[offset+1] = -8 #right
                actions[offset+2] = 1 #downright
                offset += 3
            elif mod == 0: #left rail
                tiles[offset] = i
                tiles[offset+1] = i
                tiles[offset+2] = i
                tiles[offset+3] = i
                actions[offset] = -9 #upright
                actions[offset+1] = -8 #right
                actions[offset+2] = 1 #downright
                actions[offset+3] = 9 #downleft
                offset += 4
            elif mod == 8: #right rail
                tiles[offset] = i
                tiles[offset+1] = i
                tiles[offset+2] = i
                tiles[offset+3] = i
                actions[offset] = -9 #upright
                actions[offset+1] = -1 #upleft
                actions[offset+2] = 8 #left
                actions[offset+3] = 9 #downleft
                offset += 4
            elif i < 9: #top
                tiles[offset] = i
                tiles[offset+1] = i
                tiles[offset+2] = i
                tiles[offset+3] = i
                actions[offset] = -1 #upleft
                actions[offset+1] = 8 #left
                actions[offset+2] = 9 #downleft
                actions[offset+3] = 1 #downright
                offset += 4
            elif i > 71: #bottom
                tiles[offset] = i
                tiles[offset+1] = i
                tiles[offset+2] = i
                tiles[offset+3] = i
                actions[offset] = -1 #upleft
                actions[offset+1] = -9 #upright
                actions[offset+2] = -8 #right
                actions[offset+3] = 1 #downright
                offset += 4
            else: #middle square
                tiles[offset] = i
                tiles[offset+1] = i
                tiles[offset+2] = i
                tiles[offset+3] = i
                tiles[offset+4] = i
                tiles[offset+5] = i
                actions[offset] = -1
                actions[offset+1] = -9
                actions[offset+2] = 8
                actions[offset+3] = -8
                actions[offset+4] = 9
                actions[offset+5] = 1
                offset += 6
        tiles[416] = 0 #skip
        actions[416] = 0
        return (tiles, actions)


