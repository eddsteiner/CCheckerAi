from distutils.util import split_quoted
from threading import active_count
from tracemalloc import start
from distro import major_version
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
        self.jump_move_mem = set()
        self.lock = -1
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
            if self.board2[index] != 1:
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


    def make_move(self, start_pos: int, action: int, player: bool) -> bool:
        """Returns: True = made move, False = invalid move."""
        #check for valid piece picked
        board = self.board1 if self.player else self.board2

        
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

                    
                    if self.check_jumps(start_pos + action*2):
                        self.update_board(start_pos, action)
                        #remember all space currently on
                        self.jump_moves_mem.add(start_pos+action*2)
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
                self.switch_player()
                return 0
            else:       #if action is not a slide
                
                #update board
                #check for further jump
                #if no further jump return 0
                if self.check_jumps(start_pos + action*2):
                    self.update_board(start_pos, action)
                    #remember all space currently on
                    self.jump_moves_mem.add(start_pos+action*2)
                    self.jump_moves_mem.add(start_pos)
                    self.lock = start_pos + action*2
                    return 1
                else:
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
        possible_jumps = np.empty()
        for action in self.moves:       #goes through all moves at current spot spot
            if self.current_player: #PLAYER 1
                if board[start_pos + action] != 0 and board[start_pos + (action*2)] == 0 and start_pos + (action*2) not in self.jump_move_mem: #checks the spot jumping over creatur                         
                    np.append(possible_jumps, action, axis = 0 ) #adds move tuple to a list
           

        

            

        if len(possible_jumps) > 0:
            # if len(possible_jumps) == 1: #if there is only 1 element
            #     self.update_board(possible_jumps[0][0], possible_jumps[0][1]) #make the move on the board using the start_pos and the action
            #     start_pos += possible_jumps[0][1]   #new starting position == the old pos + new action
            #     self.check_jumps(start_pos) #recursively go again
            print("jumps are possible")
            return True   #returns jump options
        else:
            print("no jump possible")
            return False     #or returns nothing

                    
    
                    
                
