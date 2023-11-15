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
        self.moves = [-1, -9, 8, -8, 9, 1]
        self.jumps = [-2, -18, 16, -16, 18, 2]
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
            self.board2[index] = 2 #fills objective 1 with player 1 pieces
        for index in self.objective_zone2:
            self.board2[index] = 1 #fills objective 2 with player 2 pieces


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


#------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------
#PLAYER 1 IS MOVE VALID


    def is_valid_move(self, board, start_pos: int, action: int) -> bool:
        """Returns: True = valid move, False = invalid move."""
        # Implement the rules to check if a move is valid
        

        if action not in self.moves: #first checks if the action value is even in the list of valid move values
            return False
         #check if the space is open
        
        else:
            #check first side -----------------------------------
            if start_pos % 9 == 0:
                #check the 0 corner that only allows 2 moves
                if start_pos == 0:
                    if action == (1 or 9):
                        if board[start_pos + action] != 0: #checks if space is empty (if not empty continue in condition)
                            if board[start_pos + (action*2)] != 0: #if not empty then check the jump space over piece
                                return False    #if not empty return false
                            else: 
                                return True     #else return true if it is empty
                        else:
                            return True #if space is empty return true
                    else:
                        return False
                #check the 72 corner that only allows 3 moves
                elif start_pos == 72:
                    if action == (1 or -9 or -8):
                        if board[start_pos + action] != 0: #checks if space is empty (if not empty continue in condition)
                            if board[start_pos + (action*2)] != 0: #if not empty then check the jump space over piece
                                return False    #if not empty return false
                            else: 
                                return True     #else return true if it is empty
                        else:
                            return True #if space is empty return true 
                    else: 
                        return False
                    
                elif action == (8 or (-1)):
                    return False
                else:
                    if board[start_pos + action] != 0: #checks if space is empty (if not empty continue in condition)
                        if board[start_pos + (action*2)] != 0: #if not empty then check the jump space over piece
                            return False    #if not empty return false
                        else: 
                            return True     #else return true if it is empty
                    else:
                        return True #if space is empty return true
                
            

             #check second side -----------------------------------
            elif (start_pos + 1) % 9 == 0:
                #check the 80 corner that only allows 2 moves
                if start_pos == 80:
                    if action == (-1 or -9):
                        if board[start_pos + action] != 0: #checks if space is empty (if not empty continue in condition)
                            if board[start_pos + (action*2)] != 0: #if not empty then check the jump space over piece
                                return False    #if not empty return false
                            else: 
                                return True     #else return true if it is empty
                        else:
                            return True #if space is empty return true
                    else:
                        return False
                #check the 8 corner that only allows 3 moves
                elif start_pos == 8:
                    if action == (-1 or 9 or 8):
                        if board[start_pos + action] != 0: #checks if space is empty (if not empty continue in condition)
                            if board[start_pos + (action*2)] != 0: #if not empty then check the jump space over piece
                                return False    #if not empty return false
                            else: 
                                return True     #else return true if it is empty
                        else:
                            return True #if space is empty return true 
                    else: 
                        return False
                elif action == (1 or (-8)):
                    return False
                else:
                    if board[start_pos + action] != 0: #checks if space is empty (if not empty continue in condition)
                        if board[start_pos + (action*2)] != 0: #if not empty then check the jump space over piece
                            return False    #if not empty return false
                        else: 
                            return True     #else return true if it is empty
                    else:
                        return True #if space is empty return true 
                


            #check  third side ---------------------------------  
            elif start_pos in range(72, 81):
                if action == (9 or 8):
                    return False
                else:
                    if board[start_pos + action] != 0: #checks if space is empty (if not empty continue in condition)
                        if board[start_pos + (action*2)] != 0: #if not empty then check the jump space over piece
                            return False    #if not empty return false
                        else: 
                            return True     #else return true if it is empty
                    else:
                        return True #if space is empty return true
                    

            #check fourth side -----------------------------------
            elif start_pos in range(0-9):
                if action == ((-9) or (-8)):
                    return False
                else: 
                    if board[start_pos + action] != 0: #checks if space is empty (if not empty continue in condition)
                        if board[start_pos + (action*2)] != 0: #if not empty then check the jump space over piece
                            return False    #if not empty return false
                        else: 
                            return True     #else return true if it is empty
                    else:
                        return True #if space is empty return true
            



        return True 
    
#------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------
#PLLAYER 2 IS MOVE VALID

    def is_valid_move_player2(self, start_pos: int, action: int) -> bool:
        """Returns: True = valid move, False = invalid move."""
        # Implement the rules to check if a move is valid
        

        if action not in self.moves: #first checks if the action value is even in the list of valid move values
            return False
         #check if the space is open
        
        else:
            #check first side -----------------------------------
            if start_pos % 9 == 0:
                #check the 0 corner that only allows 2 moves
                if start_pos == 0:
                    if action == (1 or 9):
                        if self.board2[start_pos + action] != 0: #checks if space is empty (if not empty continue in condition)
                            if self.board2[start_pos + (action*2)] != 0: #if not empty then check the jump space over piece
                                return False    #if not empty return false
                            else: 
                                return True     #else return true if it is empty
                        else:
                            return True #if space is empty return true
                    else:
                        return False
                #check the 72 corner that only allows 3 moves
                elif start_pos == 72:
                    if action == (1 or -9 or -8):
                        if self.board2[start_pos + action] != 0: #checks if space is empty (if not empty continue in condition)
                            if self.board2[start_pos + (action*2)] != 0: #if not empty then check the jump space over piece
                                return False    #if not empty return false
                            else: 
                                return True     #else return true if it is empty
                        else:
                            return True #if space is empty return true 
                    else: 
                        return False
                    
                elif action == (8 or (-1)):
                    return False
                else:
                    if self.board2[start_pos + action] != 0: #checks if space is empty (if not empty continue in condition)
                        if self.board2[start_pos + (action*2)] != 0: #if not empty then check the jump space over piece
                            return False    #if not empty return false
                        else: 
                            return True     #else return true if it is empty
                    else:
                        return True #if space is empty return true
                
            

             #check second side -----------------------------------
            elif (start_pos + 1) % 9 == 0:
                #check the 80 corner that only allows 2 moves
                if start_pos == 80:
                    if action == (-1 or -9):
                        if self.board2[start_pos + action] != 0: #checks if space is empty (if not empty continue in condition)
                            if self.board2[start_pos + (action*2)] != 0: #if not empty then check the jump space over piece
                                return False    #if not empty return false
                            else: 
                                return True     #else return true if it is empty
                        else:
                            return True #if space is empty return true
                    else:
                        return False
                #check the 8 corner that only allows 3 moves
                elif start_pos == 8:
                    if action == (-1 or 9 or 8):
                        if self.board2[start_pos + action] != 0: #checks if space is empty (if not empty continue in condition)
                            if self.board2[start_pos + (action*2)] != 0: #if not empty then check the jump space over piece
                                return False    #if not empty return false
                            else: 
                                return True     #else return true if it is empty
                        else:
                            return True #if space is empty return true 
                    else: 
                        return False
                elif action == (1 or (-8)):
                    return False
                else:
                    if self.board2[start_pos + action] != 0: #checks if space is empty (if not empty continue in condition)
                        if self.board2[start_pos + (action*2)] != 0: #if not empty then check the jump space over piece
                            return False    #if not empty return false
                        else: 
                            return True     #else return true if it is empty
                    else:
                        return True #if space is empty return true 
                


            #check  third side ---------------------------------  
            elif start_pos in range(72, 81):
                if action == (9 or 8):
                    return False
                else:
                    if self.board2[start_pos + action] != 0: #checks if space is empty (if not empty continue in condition)
                        if self.board2[start_pos + (action*2)] != 0: #if not empty then check the jump space over piece
                            return False    #if not empty return false
                        else: 
                            return True     #else return true if it is empty
                    else:
                        return True #if space is empty return true
                    

            #check fourth side -----------------------------------
            elif start_pos in range(0-9):
                if action == ((-9) or (-8)):
                    return False
                else: 
                    if self.board2[start_pos + action] != 0: #checks if space is empty (if not empty continue in condition)
                        if self.board2[start_pos + (action*2)] != 0: #if not empty then check the jump space over piece
                            return False    #if not empty return false
                        else: 
                            return True     #else return true if it is empty
                    else:
                        return True #if space is empty return true
            



        return True 

#------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------
#MAKE MOVE


    def make_move(self, start_pos: int, action: int, player: bool) -> bool:
        """Returns: True = made move, False = invalid move."""
        #check for valid piece picked
        if(player):
            if self.board1[start_pos] != 1:     #check if player 1 picked player 1 piece
                is_valid = False                #if no then piece move is not valid
            else:
                is_valid = self.is_valid_move(self.board1, start_pos, action)    #else check if the action is valid

        else:
            if self.board2[start_pos] != 2:     #do the same for player 2
                is_valid = False
            else:
                is_valid = self.is_valid_move(self.board2, start_pos, action)
                
        return is_valid
    

#------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------
#RETRIEVE BOARD


    def retrieve_board(self, player: bool) -> npt.NDArray[np.float64]:
        """Returns the board for the specified player."""
        if player: #if the player is player1
            return self.board1
        return self.board2
        #return (self.board1, self.board2)
    
#------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------
#print board

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


#------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------
#UPDATE BOARD

    def update_board(self, start_pos: int, action:int)->bool:
        if not self.make_move(start_pos, action, self.current_player):
            print("move is not valid! Did not make move")
            return False
        else:
            # if self.current_player:
            #     self.board1[start_pos + action] = 1
            #     self.board1[start_pos] = 0
            #     self.board2[(80-start_pos) + ((-1)*action)] = 2
            #     self.board2[start_pos] = 0
            #     return True
            if self.current_player:
                main_board = self.board1
                second_board = self.board2
            else:
                main_board = self.board2
                second_board = self.board1
            main_board[start_pos + action] = 1
            main_board[start_pos] = 0
            second_board[(80-start_pos) + ((-1)*action)] = 2
            second_board[start_pos] = 0

            return True