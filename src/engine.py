import numpy as np
import numpy.typing as npt
from typing import Any


class ChineseCheckersEngine:
    """Manages a Chinese Checkers game."""

    def __init__(self, player1: Any, player2: Any):
        """Initialize the game boards, objective zones, players, etc."""
        self.board1 = np.zeros(81) # 9x9 board
        self.board2 = np.zeros(81) # 9x9 board
        self.objective_zone1 = [0, 1, 2, 3, 9, 10, 11, 18, 19, 27]
        self.objective_zone2 = [53, 61, 62, 69, 70, 71, 77, 78, 79, 80]
        self.current_player = True  # Start with Player 1
        self.player1 = player1
        self.player2 = player2
        self.initialize_board()


    def initialize_board(self):
        """Initialize the game boards."""
        for index in self.objective_zone1:
            self.board1[index] = 2 #fills objective 1 with player 1 pieces
        for index in self.objective_zone2:
            self.board1[index] = 1 #fills objective 2 with player 2 pieces

        for index in self.objective_zone1:
            self.board2[index] = 1 #fills objective 1 with player 1 pieces
        for index in self.objective_zone2:
            self.board2[index] = 2 #fills objective 2 with player 2 pieces


    def switch_player(self):
        """Switch to the next player's turn."""
        self.current_player = not self.current_player


    def check_win(self):
        """Checks if there are 10 pieces in home."""
        p1_win = True
        for index in self.objective_zone1: #top, where player1 is going
            if self.board1[index] != 1:
                p1_win = False
                continue
        if p1_win: #player1 has won
            return 1
            
        p2_win = True
        for index in self.objective_zone2: #bottom, where player2 is going
            if self.board2[index] != 2:
                p2_win = False
                continue
        if p2_win: #player2 has won
            return 2
    
        return 0  # No player has won yet


    def is_valid_move(self, start_pos: int, action: int) -> bool:
        """Returns: True = valid move, False = invalid move."""
        # Implement the rules to check if a move is valid
        return True 


    def make_move(self, start_pos: int, action: int, player: bool) -> bool:
        """Returns: True = made move, False = invalid move."""
        is_valid = self.is_valid_move(start_pos, action)
        if not is_valid:
            return False
        # Make a move on the board if it's valid
        return True


    def retrieve_board(self, player: bool) -> npt.NDArray[np.float64]:
        """Returns the board for the specified player."""
        if player: #if the player is player1
            return self.board1
        return self.board2
        #return (self.board1, self.board2)
    
    
    # def play(self):
    #     while not self.check_win():
    #         # Main game loop
    #         self.display_board()
    #         if self.current_player == 1:
    #             # AI1's turn
    #         else:
                
    #             # AI2 turn
                
    #         self.switch_player()
    

    def print_board(self):
        #player 1 board
        print("Player 1 Board")
        for row in range(9):
            # Print spaces for formatting
            for _ in range(row):
                print(" ", end=" ")
            for col in range(9):
                index = row * 9 + col
                print(f"{self.board1[index]}", end=" ")
            print()  # Move to the next line for the next row

        print()
        print("Player 2 Board")
        #player 2 board    
        for row in range(9):
            # Print spaces for formatting
            for _ in range(row):
                print(" ", end=" ")
            for col in range(9):
                index = row * 9 + col
                if self.board2[index] == 0:
                    print("0", end=" ")
                elif self.board2[index] == 1:
                    print("1", end=" ")
                elif self.board2[index] == 2:
                    print("2", end=" ")
            print()  # Move to the next line for the next row

