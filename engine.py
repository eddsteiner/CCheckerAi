import numpy as numpy

class ChineseCheckersEngine:
    def __init__(self):
        # Initialize the game board1, objective zones, players, etc.
        self.board1 = [0] * 81  # 9x9 board
        self.board2 = [0] * 81  # 9x9 board
        self.objective_zone1 = [0, 1, 2, 3, 9, 10, 11, 18, 19, 27]
        self.objective_zone2 = [53, 61, 62, 69, 70, 71, 77, 78, 79, 80]
        self.current_player = 1  # Start with Player 1
        self.initialize_board()



    def is_in_objective_zone1(self, index):
        return index in self.objective_zone1

    def is_in_objective_zone2(self, index):
        return index in self.objective_zone2

    
    def initialize_board(self):
        for index in self.objective_zone1:
            self.board1[index] = 1 #fills objective 1 with player 1 pieces
        for index in self.objective_zone2:
            self.board1[index] = 2 #fills objective 2 with player 2 pieces

        for index in self.objective_zone1:
            self.board2[index] = 2 #fills objective 1 with player 1 pieces
        for index in self.objective_zone2:
            self.board2[index] = 1 #fills objective 2 with player 2 pieces

    def switch_player(self):
        # Switch to the next player's turn
        self.current_player = 3 - self.current_player  # Toggle between 1 and 2

    def check_win(self):
        #checks if there are 10 pieces in objective zone
        count_check1 = 0
        count_check2 = 0
        for index in objective_zone1:
            if self.board1[index] == 2:
                count_check1 += 1
            else:
                break
        for index in objective_zone2:
            if self.board1[index] == 1:
                count_check2 += 1
            else:
                break
        if count_check1 == len(self.objective_zone1):
            return 2  # Player 2 (
    
        if count_check2 == len(self.objective_zone2):
            return 1  # Player 1
    
        return 0  # No player has won yet

    

    def is_valid_move(self, start_pos, end_pos):
        # Implement the rules to check if a move is valid
        pass

    def make_move(self, start_pos, end_pos):
        # Make a move on the board if it's valid
        pass

    

    def find_best_move(self):
        # Implement AI logic to find the best move
        pass

    
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
                if self.board1[index] == 0:
                    print("0", end=" ")
                elif self.board1[index] == 1:
                    print("1", end=" ")
                elif self.board1[index] == 2:
                    print("2", end=" ")
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