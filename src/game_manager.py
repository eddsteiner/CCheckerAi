import numpy as np
import numpy.typing as npt
import random

from neat import Creature
from engine import ChineseCheckersEngine


class Stats:
    """Contains stats about a Chinese Checkers game."""
    pass


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


    def run_game(self, creature1: Creature, creature2: Creature) -> tuple[bool, Stats]:
        """Runs one game on two creatures."""
       
       # NOTE, WRITE CODE HERE

        return (True, Stats())


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
        return (tiles, actions)

#    def __init__(self) -> None:
#        self.move_map = self.get_move_map().astype(np.int32)
#        # self.p1 = Creature1
#        # self.p2 = Creature2
#
#    #needs to return 1 or 0. 1 means p1 wins 0 means p2 wins
#    def run_game(self, p1: Creature, p2: Creature) -> tuple[bool, Stats]:
#        """Will run a game on the two provided creatures"""
#        #self.p1 = p1
#        #self.p2 = p2
#        game = ChineseCheckersEngine(p1, p2)
#
#        board1pointer = game.board1.ctypes.data
#        board2pointer = game.board2.ctypes.data
#
#        output_buffer_array = np.random.randint(1,417, size = 417)
#        #print(output_buffer_array)
#        #output_buffer_array = np.empty(417, dtype = np.float32)
#        output_buffer = output_buffer_array.ctypes.data
#        buffer_rankings = np.zeros(len(output_buffer_array))
#        action_result = 0
#        index_count = 0
#        start_pos = 0
#        action = 0
#        move_to_grab = 1
#        
#        player = p1 if game.current_player else p2
#        board_pointer = board1pointer if game.current_player else board2pointer
#        #print(output_buffer)
#        
#        player.calculate(board_pointer, output_buffer)
#        #rank the buffer readings
#        sorted_indices = np.argsort(output_buffer_array)[::-1]
#        buffer_rankings[sorted_indices] = np.arange(1, len(sorted_indices) + 1)
#        #print(buffer_rankings)
#
#
#
#
#
#
#        while action_result not in (2, 3): 
#            # game.print_board()
#            #------------------------BROKEN
#            #extract startpos and action
#            index_count = 0
#            for index in buffer_rankings:
#                if index == move_to_grab:
#                    # print("index_count: ", index_count)
#                    start_pos = self.move_map[index_count][0]
#                    action = self.move_map[index_count][1]
#                    index_count = 0
#                else:
#                    index_count += 1
#            
#            #insert start pos and action into make_move
#            action_result = game.make_move(start_pos, action, p1)
#            #while make_move returns -1
#            index_count = 0
#            while action_result == -1:
#                index_count = 0
#                move_to_grab += 1
#                # print("move to grab: ", move_to_grab)           #get the next best move
#                
#                
#                for index in buffer_rankings:   #look for the next best ranking
#                    if index == move_to_grab:   #if we find it
#                        start_pos = self.move_map[index_count][0] #extract start pos and action
#                        #print(buffer_rankings)
#                        # print("index_count: ", index_count)
#                        action = self.move_map[index_count][1]
#                        # print("start_pos: ", start_pos)
#                        # print("action: ", action)
#                        index_count = 0
#                    
#                    index_count += 1
#
#                action_result = game.make_move(start_pos, action, p1) #check to see if it will go -1
#            
#            if action_result == 2:
#                return (True, Stats())
#            if action_result == 3:
#                return(False, Stats())
#            
#            
#            if action_result == 0:
#                index_count = 0
#                for index in buffer_rankings:
#                    if index == move_to_grab:
#                        # print("index_count: ", index_count)
#                        start_pos = self.move_map[index_count][0]
#                        action = self.move_map[index_count][1]
#                        index_count = 0
#                    else:
#                        index_count += 1
#                
#                #insert start pos and action into make_move
#                action_result = game.make_move(start_pos, action, p1)
#                #while make_move returns -1
#                index_count = 0
#                while action_result == -1:
#                    index_count = 0
#                    move_to_grab += 1
#                    # print("move to grab: ", move_to_grab)           #get the next best move
#                    
#                    
#                    for index in buffer_rankings:   #look for the next best ranking
#                        if index == move_to_grab:   #if we find it
#                            start_pos = self.move_map[index_count][0] #extract start pos and action
#                            #print(buffer_rankings)
#                            # print("index_count: ", index_count)
#                            action = self.move_map[index_count][1]
#                            # print("start_pos: ", start_pos)
#                            # print("action: ", action)
#                            index_count = 0
#                        
#                        index_count += 1
#
#                    action_result = game.make_move(start_pos, action, p1) #check to see if it will go -1
#                    
#
#
#
#            
#        
#
#        
#        
#        
#        
#        
#        #return (random.choice([True, False]), Stats())
#
#
#    #maps every possible move to an index in an array tuple(start_pos, action). Tile 0 is where move 0 starts
#    def get_move_map(self):
#        player1 = 0
#        player2 = 0
#        skip = -1   #value of start_pos when skipping a jump
#        game = ChineseCheckersEngine(player1, player2)  #using engine for validating moves
#        empty_board = np.zeros(81)  #using to iterate through board
#        moveset = [-1, -9, 8, -8, 9, 1] #our llist of possible directions you can move
#        move_map = np.empty((0,2), dtype = int) #going to fill this with tuples
#
#        for index in range(len(empty_board)): #going through index 0-80
#            for move in moveset:               #going through every move in the moveset array
#                if game.is_valid_move(empty_board, index, move):    #if the move is valid
#                    added_tuple = (index, move)                     #add the move to the tuple (start_pos, action)
#                    move_map = np.append(move_map, [added_tuple], axis=0)   #append that tuple to the move_map
#                    # print("tuple ", added_tuple, " added")
#                # else:
#                    # print("move invalid")
#        
#        skip_tuples = (skip, moveset[0])                            #add extra move for skipping
#        move_map = np.append(move_map, [skip_tuples], axis = 0)     #appends the skip tuple
#        print("skip tuple added")
#
#
#        return move_map


