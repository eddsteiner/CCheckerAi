from distutils.util import split_quoted
from threading import active_count
from tracemalloc import start
#from distro import major_version
import numpy as np
import numpy.typing as npt
from typing import Any
from functools import reduce


class ChineseCheckersEngine:
    """Manages a Chinese Checkers game."""

    def __init__(self):
        """Initialize the game boards, objective zones, players, etc."""
        self.board1 = np.zeros(81, dtype = np.float32) # 9x9 board
        self.board2 = np.zeros(81, dtype = np.float32) # 9x9 board
        self.home_top = np.array([0, 1, 2, 3, 9, 10, 11, 18, 19, 27], dtype = np.int32)
        self.home_bot = np.array([53, 61, 62, 69, 70, 71, 77, 78, 79, 80], dtype = np.int32)
        self.actions = np.array([-1, -9, 8, -8, 9, 1], dtype = np.int32) #upleft, upright, left, right, downleft, downright
        self.middle_row = np.array([72, 64, 56, 48, 40, 32, 24, 16, 8], dtype = np.int32) #for collecting stats

        self.lock = -1
        self.jump_history = set()
        self.turn = True  #start with player1

        self.initialize_board()


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


    def check_win(self) -> bool:
        """Checks if there are 10 pieces in home."""
        board = self.board1 if self.turn else self.board2
        x = list(filter(lambda x: not x, map(lambda x: board[x] == 1, self.home_top))) #find if there's a single piece that isn't the player's
        return len(x) == 0
    


#------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------
#PLAYER 1 IS MOVE VALID


    def is_valid_move(self, board, start_pos: int, action: int) -> bool:
        """Returns: True = valid move, False = invalid move."""
        # Implement the rules to check if a move is valid
        
        
                

        if action not in self.moves: #first checks if the action value is even in the list of valid move values
            print('YO PICK A VALID MOVE FROM THE MOVE ARRAY')
            return False
         #check if the space is open
        
        else:
            #check first side -----------------------------------
            if start_pos % 9 == 0:
                #check the 0 corner that only allows 2 moves
                if start_pos == 0:
                    if action in (1, 9):
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
                    if action in (1, -9, -8):
                        if board[start_pos + action] != 0: #checks if space is empty (if not empty continue in condition)
                            if board[start_pos + (action*2)] != 0: #if not empty then check the jump space over piece
                                return False    #if not empty return false
                            else: 
                                return True     #else return true if it is empty
                        else:
                            return True #if space is empty return true 
                    else: 
                        return False
                    
                elif action in (8, (-1)):
                    return False
                else:
                    if board[start_pos + action] != 0: #checks if space is empty (if not empty continue in condition)
                        if start_pos == 63:
                            if action in (-1, 9):
                                return False
                        if start_pos == 9:
                            if action in (-9, -1, -8):
                                return False
                        if board[start_pos + (action*2)] != 0: #if not empty then check the jump space over piece
                            return False    #if not empty return false
                        else: 
                            return True     #else return true if it is empty
                    else:
                        return True #if space is empty return true
                
            

             #check second side -----------------------------------
            elif (start_pos + 1) % 9 == 0:
                #print("in the right area")
                #check the 80 corner that only allows 2 moves
                if start_pos == 80:
                    #print("in the wrong area1")
                    if action in (-1, -9):
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
                    #print("in the wrong area2")
                    if action in (-1, 9, 8):
                        if board[start_pos + action] != 0: #checks if space is empty (if not empty continue in condition)
                            if board[start_pos + (action*2)] != 0: #if not empty then check the jump space over piece
                                return False    #if not empty return false
                            else: 
                                return True     #else return true if it is empty
                        else:
                            return True #if space is empty return true 
                    else: 
                        return False
                elif action in (1, (-8)):
                    return False
                
                            
                else:
                    #print("almost")
                    if board[start_pos + action] != 0: #checks if space is empty (if not empty continue in condition)
                        #print("almost2")
                        if start_pos == 71:
                            if action in (8,9):
                                if board[start_pos + action] != 0:
                                    #print("correct spot")
                                    return False
                        elif start_pos == 17:
                            if action in (-9, 1):
                                return False
                        elif board[start_pos + (action*2)] != 0: #if not empty then check the jump space over piece
                            
                            return False    #if not empty return false
                        
                        else: 
                            #print("returns true 1")
                            return True     #else return true if it is empty
                    
                    else:
                        #print("returns true2")
                        return True
                


            #check  third side ---------------------------------  
            elif start_pos in range(72, 81):
                if action in (9, 8):
                    return False
                else:
                    if board[start_pos + action] != 0: #checks if space is empty (if not empty continue in condition)
                        if start_pos == 79:
                            if action in (-8,1):
                                if board[start_pos + action] != 0:
                                    #print("correct spot")
                                    return False
                        if start_pos == 73:
                            if action in (-1, 8, 9):
                                return False
                        if board[start_pos + (action*2)] != 0: #if not empty then check the jump space over piece
                            return False    #if not empty return false
                        else: 
                            return True     #else return true if it is empty
                    else:
                        return True #if space is empty return true
                    

            #check fourth side -----------------------------------
            elif start_pos in range(0, 9):
                if action in ((-9), (-8)):
                    return False
                
                else: 
                    if board[start_pos + action] != 0: 
                        if start_pos == 7:
                            if action in (1, -8, -9):
                                return False
                        if start_pos == 1:
                            if action in (-1, -9, -8):
                                return False
                        if board[start_pos + (action*2)] != 0: #if not empty then check the jump space over piece
                            return False    #if not empty return false
                        else: 
                            return True     #else return true if it is empty
                    else:
                        return True #if space is empty return true
            #-------------------------------------------------------------
            #check inside side 1 -----------------------------------------
            #-------------------------------------------------------------
            elif (start_pos + 2) % 9 == 0:
                #check inside intersection-------
                if start_pos == 70:
                    if action in (1, 8, 9):
                        if board[start_pos + action] != 0: #checks if space is empty (if not empty continue in condition)
                            return False    #if not empty return false
                        else: 
                            return True     #else return true if it is empty        
                           
                    else:
                            return True #if space is empty return true    
                    
                #check inside intersection-------
                elif start_pos == 16:
                    if action in (-9, -8, 1):
                        if board[start_pos + action] != 0: #checks if space is empty (if not empty continue in condition)
                            return False    #if not empty return false
                        else: 
                            return True     #else return true if it is empty
                    else:
                        return True #if space is empty return true
                    
                else:
                    if action in (1, -8):
                        #print(start_pos, " ", action)
                        if board[start_pos + action] != 0: #checks if space is empty (if not empty continue in condition)
                            return False
                        else: 
                            return True     #else return true if it is empty
                    else:
                        return True #if space is empty return true                
                            
                   
            #-------------------------------------------------------------
            #check inside side 2 -----------------------------------------
            #-------------------------------------------------------------
            elif (start_pos -1) % 9 == 0:
                #check inside intersection-----
                if start_pos == 10:
                    if action in (-1, 8, 9):
                        if board[start_pos + action] != 0: #checks if space is empty (if not empty continue in condition)
                            return False    #if not empty return false
                        else: 
                            return True     #else return true if it is empty        
                           
                    else:
                            return True #if space is empty return true 
                #check inside intersection-----
                elif start_pos == 64:
                    if action in (-1, 8, 9):
                        if board[start_pos + action] != 0: #checks if space is empty (if not empty continue in condition)
                            return False    #if not empty return false
                        else: 
                            return True     #else return true if it is empty        
                           
                    else:
                            return True #if space is empty return true 
                else:
                    if action in (-1, 8):
                        if board[start_pos + action] != 0: #checks if space is empty (if not empty continue in condition)
                            return False    #if not empty return false
                        else: 
                            return True     #else return true if it is empty        
                           
                    else:
                            return True #if space is empty return true 



            #-------------------------------------------------------------
            #check inside side 3 -----------------------------------------
            #-------------------------------------------------------------
            elif start_pos in range(9, 18):
                if action in (-9, -8):
                    if board[start_pos + action] != 0: #checks if space is empty (if not empty continue in condition)
                            return False    #if not empty return false
                    else: 
                        return True     #else return true if it is empty        
                           
                else:
                    return True #if space is empty return true 
            #-------------------------------------------------------------
            #check inside side 4 -----------------------------------------
            #-------------------------------------------------------------
            elif start_pos in range(63, 72):
                if action in (9, 8):
                    if board[start_pos + action] != 0: #checks if space is empty (if not empty continue in condition)
                            return False    #if not empty return false
                    else: 
                        return True     #else return true if it is empty        
                           
                else:
                        return True #if space is empty return true
            else:
                if board[start_pos + action] != 0: #checks if space is empty (if not empty continue in condition)
                    if board[start_pos + (action*2)] != 0: #if not empty then check the jump space over piece
                        return False    #if not empty return false
                    else: 
                        return True     #else return true if it is empty
                else:
                    return True #if space is empty return true 


            



        return False 
    
#------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------


#------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------
#MAKE MOVE

    #this move returns integers that mean different outcomes:
    # -1: move is invalid and cannot be made
    # 0: move was accepted, player is switched, lock is cleared, and jump mem is cleared
    # 1: jump has been initiated and there is a chance of another jump
    # 2: player 1 wins
    # 3: player 2 wins

    def make_move(self, start_pos: int, action: int, player: bool) -> bool:

        #defines the board
        board = self.board1 if self.current_player else self.board2
        #checks for wins
        if self.check_win() == 1:   #if function returns 1 
            print("player 1 wins!")
            return 2
        if self.check_win() == 2:   #if function returns 2
            print("player 2 wins")
            return 3

        #check for valid piece picked
        if start_pos != -1 and board[start_pos] != 1:     #check if player 1 picked player 1 piece
            print('CMON MAN PICK A PIECE THAT IS YOURS. YOUR PIECE SAYS 1')
            
            return -1               #if no then piece move is not valid
        else:
            if start_pos == -1 and self.lock > -1: #check if it is a valid skip move
                self.switch_player()
                self.jump_move_mem.clear()
                self.lock = -1
                return 0
            
            if start_pos == -1 and self.lock == -1:
                return -1
            
            if not self.is_valid_move(board, start_pos, action):  #else check if the action is valid
                return -1
            

            if self.lock > -1:    #there is a lock
                
                if start_pos != self.lock:
                    return -1
                
                if board[start_pos + action] != 0 and board[start_pos + action*2] == 0:

                    
                    if self.check_jumps(start_pos + action*2, board):
                        self.update_board(start_pos, action)
                        print("move made")
                        #remember all space currently on
                        self.jump_move_mem.add(start_pos+action*2)
                        #self.jump_moves_mem.add(start_pos)
                        self.lock = start_pos + action*2
                        return 1
                    else:
                        self.switch_player()
                        self.jump_move_mem.clear()
                        self.lock = -1
                        return 0
                    
                    
            if board[start_pos + action ] == 0: #check for a simple slide
                self.update_board(start_pos, action)
                print("move made")
                self.switch_player()
                return 0
            else:       #if action is not a slide
                
                #update board
                #check for further jump
                #if no further jump return 0
                if self.check_jumps(start_pos + action*2, board):
                    self.update_board(start_pos, action)
                    print("move made")
                    #remember all space currently on
                    self.jump_move_mem.add(start_pos+action*2)
                    self.jump_move_mem.add(start_pos)
                    self.lock = start_pos + action*2
                    return 1
                else:
                    print("here")
                    print("start_pos: ", start_pos)
                    print("action: ", action)
                    self.switch_player()
                    self.jump_move_mem.clear()
                    self.lock = -1
                    return 0

                return 1 #return 1       
                        
                
                    
                    
            

        

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
        # if not self.make_move(start_pos, action, self.current_player):
        #     print("move is not valid! Did not make move")
        #     return False
        # else:
        #     print("make_move returned true for some reason!!!")
            if self.current_player:
                main_board = self.board1
                second_board = self.board2
            else:
                main_board = self.board2
                second_board = self.board1

            if main_board[start_pos + action] != 0:
                main_board[start_pos + (2*action)] = 1
                main_board[start_pos] = 0
                second_board[(80-start_pos) + (2*((-1)*action))] = 2
                second_board[(80 - start_pos)] = 0
            else:
                main_board[start_pos + action] = 1
                main_board[start_pos] = 0
                second_board[(80-start_pos) + ((-1)*action)] = 2
                second_board[(80 - start_pos)] = 0
            
            return True


   
    
    def check_jumps(self, start_pos, board)->bool:
        possible_jumps = []  # Use a Python list instead of a NumPy array

        for action in self.moves:
            if start_pos + action < 81:
                if board[start_pos + action] != 0:
                    if start_pos + (action * 2) < 81:
                        if board[start_pos + (action * 2)] == 0:
                            if start_pos + (action * 2) not in self.jump_move_mem:
                                possible_jumps.append(action)  # Append action to the list

        if len(possible_jumps) > 0:
            # Convert the list to a NumPy array if needed
            possible_jumps = np.array(possible_jumps, dtype=np.float32)
            print("jumps are possible")
            return True  # returns jump options
        else:
            print("no jump possible")
            return False  # or returns nothing




        # possible_jumps = np.empty((), dtype=np.float32)
        # for action in self.moves:       #goes through all moves at current spot spot
        #     if self.current_player: #PLAYER 1



        #         if board[start_pos + action] != 0:
        #             if start_pos + (action*2) < 81:
        #                 if board[start_pos + (action*2)] == 0:
        #                     if start_pos + (action*2) not in self.jump_move_mem: #checks the spot jumping over creatur                         
        #                         np.append(possible_jumps, action, axis = 0 ) #adds move tuple to a list
           

        

            

        # if len(possible_jumps) > 0:
        #     # if len(possible_jumps) == 1: #if there is only 1 element
        #     #     self.update_board(possible_jumps[0][0], possible_jumps[0][1]) #make the move on the board using the start_pos and the action
        #     #     start_pos += possible_jumps[0][1]   #new starting position == the old pos + new action
        #     #     self.check_jumps(start_pos) #recursively go again
        #     print("jumps are possible")
        #     return True   #returns jump options
        # else:
        #     print("no jump possible")
        #     return False     #or returns nothing

                    
    
                    
                
