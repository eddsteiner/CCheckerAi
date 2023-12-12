import numpy as np


class ChineseCheckersEngine:
    """Manages a Chinese Checkers game."""

    def __init__(self):
        """Initialize the game boards, objective zones, players, etc."""
        self.board1 = np.zeros(81, dtype = np.float32) # 9x9 board
        self.board2 = np.zeros(81, dtype = np.float32) # 9x9 board
        self.home_top = np.array([0, 1, 2, 3, 9, 10, 11, 18, 19, 27], dtype = np.int32)
        self.home_bot = np.array([53, 61, 62, 69, 70, 71, 77, 78, 79, 80], dtype = np.int32)
        self.actions = {-1, -9, 8, -8, 9, 1} #upleft, upright, left, right, downleft, downright, NOTE: skips are disallowed normally

        self.lock = -1 #no lock at first
        self.jump_history: set[int] = set() #no history at first
        self.current_player = True  #start with player1

        self.middle_row = {72, 64, 56, 48, 40, 32, 24, 16, 8} #for collecting stats

        self.initialize_board()


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


    def initialize_board(self):
        """Initialize the game boards."""
        for index in self.home_top: #fill in opponent pieces
            self.board1[index] = 2
            self.board2[index] = 2
        for index in self.home_bot: #fill in player pieces
            self.board1[index] = 1
            self.board2[index] = 1


    def switch_turn(self):
        """Switch to the other player's turn."""
        self.current_player = not self.current_player

    
    def update_board(self, tile: int, new_tile: int) -> bool:
        """Update both boards at once, moving the piece from tile to new_tile."""
        if self.current_player:
            board1 = self.board1
            board2 = self.board2
        else:
            board1 = self.board2
            board2 = self.board1

        if (board1[new_tile] != 0) or (board1[tile] != 1): #if we tried to do something wrong
            return False

        board1[new_tile] = board1[tile] #update main board
        board1[tile] = 0
        board2[80 - new_tile] = board2[80 - tile] #update secondary board
        board2[80 - tile] = 0
        return True


    def is_move_possible(self, tile: int, action: int) -> bool:
        """Check if a move is possible, agnostic of the current board."""
        if (tile < 0) or (tile > 80) or (action not in self.actions): #parameters were bad, skips are also disallowed
            return False
        if tile < 9 and (action == -9 or action == -8): #upright or right
            return False
        elif tile > 71 and (action == 9 or action == 8): #downleft or left
            return False

        mod = tile % 9
        if mod == 0 and (action == -1 or action == 8): #upleft or left
            return False
        elif mod == 8 and (action == 1 or action == -8): #downright or right
            return False

        return True #doesn't fall into any impossible case so it's possible


    def is_move_valid(self, tile: int, action: int) -> bool:
        """
        Is the move valid on the current board?
        Checks player's turn, and validity.
        """
        if not self.is_move_possible(tile, action): #return if not even possible
            return False
        board = self.board1 if self.current_player else self.board2

        if board[tile] != 1: #if tile isn't the player's
            return False
        elif board[tile + action] == 0: #slide
            return True
        elif board[tile + action * 2] == 0: #slide is invalid but jump is valid
            return True

        return False #slide and jump are both invalid


    def is_jump_valid(self, tile: int, action: int) -> bool:
        """Verify the jump is valid."""

        if self.lock > -1: #if active lock
            if action == -1: #if skip
                return True
            elif tile != self.lock: #if lock doesn't match
                return False
        if not self.is_move_possible(tile, action): #if move impossible
            return False

        board = self.board1 if self.current_player else self.board2
        if self.lock > -1 and board[tile + action * 2] in self.jump_history: #if we've already visited this tile before in a previous jump
            return False
        if (board[tile] != 1) or (board[tile + action] == 0) or (board[tile + action * 2] != 0): #ensure the tiles are good
            return False
        return True


    def check_jumps(self, tile: int) -> bool:
        """Checks if there's any possible jumps out of this tile."""
        valid = list(map(lambda x: self.is_jump_valid(tile, x), self.actions)) #count number of valid jumps
        return len(valid) > 0
        

    def check_win(self) -> bool:
        """Checks if there are 10 pieces in home."""
        board = self.board1 if self.current_player else self.board2
        incomplete = list(filter(lambda x: board[x] != 1, self.home_top)) #find if there's any incomplete space
        return len(incomplete) == 0


    def make_move(self, tile: int, action: int) -> int:
        """
        Attempt to run a move on the board.

        Return:
        -1 = invalid
        0 = switched players' turns
        1 = currently jumping
        2 = game was won
        """
        if self.lock > -1: #lock is active
            if not self.is_jump_valid(tile, action): #if jump invalid
                return -1
            if action == -1: #if skip
                self.lock = -1 #remove lock
                self.jump_history.clear()
                if self.check_win(): #if win
                    return 2
                self.switch_turn()
                return 0

            # lock is active and jump is valid, so run the jump and check for more jumps
            new_tile = tile + action * 2
            self.update_board(tile, new_tile) #execute the jump
            if self.check_jumps(new_tile): #more jumps available
                self.lock = new_tile #update lock
                self.jump_history.add(new_tile) #remember this tile
                return 1
            else: #no more jumps available
                self.lock = -1 #remove lock
                self.jump_history.clear()
                if self.check_win(): #if win
                    return 2
                self.switch_turn()
                return 0

        else: #no lock
            if not self.is_move_valid(tile, action): #if move invalid
                return -1
            
            board = self.board1 if self.current_player else self.board2
            if board[tile + action] == 0: #slide is available
                self.update_board(tile, tile + action)
                if self.check_win(): #if win
                    return 2
                self.switch_turn()
                return 0
            else: #jump is available
                new_tile = tile + action * 2
                self.update_board(tile, new_tile)
                if self.check_jumps(new_tile): #if more jumps available
                    self.lock = new_tile
                    self.jump_history.add(new_tile)
                    self.jump_history.add(tile)
                    return 1
                else: #no more jumps available
                    if self.check_win(): #if win
                        return 2
                    self.switch_turn()
                    return 0


