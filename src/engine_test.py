import numpy as np
# test_script.py

from engine import ChineseCheckersEngine

# # Now you can use ChineseCheckersEngine in your test cases


# Helper function to initialize the game and set the board for testing
def initialize_test_game(board):
    player1 = "yuhhhh"
    player2 = "yeeee"
    game = ChineseCheckersEngine(player1, player2)
    game.board1 = np.zeros(81)
   
    
    for index in board:
        game.board1[index] = 1

    
    
    return game

# # Test Case 1: Valid Move 
# game = initialize_test_game([17, 16, 8, 7])
# start_pos = 7
# action = 1
# result = game.is_valid_move(game.board1, start_pos, action)
# game.update_board(start_pos, action)
# print(result)  

# # Test Case 1: Valid Move 
# game = initialize_test_game([17, 16, 8, 7])
# start_pos = 17
# action = -9
# result = game.is_valid_move(game.board1, start_pos, action)
# game.update_board(start_pos, action)
# print(result)  

# # Test Case 1: Valid Move 
# game = initialize_test_game([17, 16, 8, 7])
# start_pos = 16
# action = -8
# result = game.is_valid_move(game.board1, start_pos, action)
# game.update_board(start_pos, action)
# print(result)  



# #-----------------------------------------------------------------------------------------------------------------------------------------
# #-----------------------------------------------------------------------------------------------------------------------------------------
# #-----------------------------------------------------------------------------------------------------------------------------------------


# # Test Case 1: Valid Move 
# game = initialize_test_game([72, 73, 64, 63])
# start_pos = 73
# action = -1
# result = game.is_valid_move(game.board1, start_pos, action)
# game.update_board(start_pos, action)
# print(result)  

# # Test Case 1: Valid Move 
# game = initialize_test_game([72, 73, 64, 63])
# start_pos = 63
# action = 9
# result = game.is_valid_move(game.board1, start_pos, action)
# game.update_board(start_pos, action)
# print(result)  

# # Test Case 1: Valid Move 
# game = initialize_test_game([72, 73, 64, 63])
# start_pos = 63
# action = -1
# result = game.is_valid_move(game.board1, start_pos, action)
# game.update_board(start_pos, action)
# print(result)  

# # Test Case 1: Valid Move 
# game = initialize_test_game([72, 73, 64, 63])
# start_pos = 64
# action = 8
# result = game.is_valid_move(game.board1, start_pos, action)
# game.update_board(start_pos, action)
# print(result)  



# #-----------------------------------------------------------------------------------------------------------------------------------------
# #-----------------------------------------------------------------------------------------------------------------------------------------
# #-----------------------------------------------------------------------------------------------------------------------------------------


# # Test Case 1: Valid Move 
# game = initialize_test_game([71, 79, 80])
# start_pos = 79
# action = 1
# result = game.is_valid_move(game.board1, start_pos, action)
# game.update_board(start_pos, action)
# print(result)  

# # Test Case 1: Valid Move 
# game = initialize_test_game([71, 79, 80])
# start_pos = 71
# action = 9
# result = game.is_valid_move(game.board1, start_pos, action)
# game.update_board(start_pos, action)
# print(result)  

# # Test Case 1: Valid Move 
# game = initialize_test_game([71, 79, 80])
# start_pos = 71
# action = 8
# result = game.is_valid_move(game.board1, start_pos, action)
# game.update_board(start_pos, action)
# print(result)  

# # Test Case 1: Valid Move 
# game = initialize_test_game([71, 79, 80])
# start_pos = 80
# action = 1
# result = game.is_valid_move(game.board1, start_pos, action)
# game.update_board(start_pos, action)
# print(result)  


# #-----------------------------------------------------------------------------------------------------------------------------------------
# #-----------------------------------------------------------------------------------------------------------------------------------------
# #-----------------------------------------------------------------------------------------------------------------------------------------

# # Test Case 1: Valid Move 
# game = initialize_test_game([0, 1, 9])
# start_pos = 1
# action = -1
# result = game.is_valid_move(game.board1, start_pos, action)
# game.update_board(start_pos, action)
# print(result)  

# # Test Case 1: Valid Move 
# game = initialize_test_game([0, 1, 9])
# start_pos = 9
# action = -9
# result = game.is_valid_move(game.board1, start_pos, action)
# game.update_board(start_pos, action)
# print(result)  

# # Test Case 1: Valid Move 
# game = initialize_test_game([0, 1, 9])
# start_pos = 9
# action = -8
# result = game.is_valid_move(game.board1, start_pos, action)
# game.update_board(start_pos, action)
# print(result)  



# #-----------------------------------------------------------------------------------------------------------------------------------------
# #-----------------------------------------------------------------------------------------------------------------------------------------
# #-----------------------------------------------------------------------------------------------------------------------------------------


# board_config = np.zeros(81)

# board_config = [x for x in range(81) if (x + 1) % 9 == 0 or (x + 2) % 9 == 0]

# game = initialize_test_game(board_config)
# x = 7
# # game.print_board()
# while x < 80:
    
#     start_pos = x
#     print(start_pos)
#     action = 1
#     result = game.is_valid_move(game.board1, start_pos, action)
#     print(result)
#     x += 9


# #-----------------------------------------------------------------------------------------------------------------------------------------
# #-----------------------------------------------------------------------------------------------------------------------------------------
# #-----------------------------------------------------------------------------------------------------------------------------------------




# board_config = np.zeros(81)

# board_config = [x for x in range(81) if (x) % 9 == 0 or (x - 1) % 9 == 0]

# game = initialize_test_game(board_config)
# x = 1
# # game.print_board()
# while x < 80:
    
#     start_pos = x
#     print(start_pos)
#     action = -1
#     result = game.is_valid_move(game.board1, start_pos, action)
#     print(result)
#     x += 9


# #-----------------------------------------------------------------------------------------------------------------------------------------
# #-----------------------------------------------------------------------------------------------------------------------------------------
# #-----------------------------------------------------------------------------------------------------------------------------------------




# board_config = np.zeros(81)

# board_config = [x for x in range(81) if (x) in range(0,9) or x in range(9,18)]

# game = initialize_test_game(board_config)
# x = 9
# #game.print_board()
# while x < 18:
    
#     start_pos = x
#     print(start_pos)
#     action = -9
#     result = game.is_valid_move(game.board1, start_pos, action)
#     print(result)
#     x += 1


#     #-----------------------------------------------------------------------------------------------------------------------------------------
# #-----------------------------------------------------------------------------------------------------------------------------------------
# #-----------------------------------------------------------------------------------------------------------------------------------------




# board_config = np.zeros(81)

# board_config = [x for x in range(81) if (x) in range(63,72) or x in range(72,81)]

# game = initialize_test_game(board_config)
# x = 63
# #game.print_board()
# while x < 72:
    
#     start_pos = x
#     print(start_pos)
#     action = 9
#     result = game.is_valid_move(game.board1, start_pos, action)
#     print(result)
#     x += 1



# #-----------------------------------------------------------------------------------------------------------------------------------------
# #-----------------------------------------------------------------------------------------------------------------------------------------
# #-----------------------------------------------------------------------------------------------------------------------------------------


# board_config = np.zeros(81)

# board_config = [x for x in range(81) if (x + 4) % 9 == 0 or (x + 2) % 9 == 0 or (x+5) %9 == 0]

# game = initialize_test_game(board_config)
# x = 4
# game.print_board()
# while x < 80:
    
#     start_pos = x
#     print(start_pos)
#     action = 1
#     result = game.is_valid_move(game.board1, start_pos, action)
#     game.update_board(start_pos, action)
#     print(result)
#     x += 9
# game.print_board()   
# i = 6




# while i < 80:
    
#     start_pos = i
#     print(start_pos)
#     action = 1
#     result = game.is_valid_move(game.board1, start_pos, action)
#     game.update_board(start_pos, action)
#     print(result)
#     i += 9
# game.print_board()




# #-----------------------------------------------------------------------------------------------------------------------------------------
# #-----------------------------------------------------------------------------------------------------------------------------------------
# #-----------------------------------------------------------------------------------------------------------------------------------------


board_config = np.zeros(81)

board_config = [x for x in range(81) if (x + 4) % 9 == 0 or (x + 2) % 9 == 0 or (x+5) %9 == 0]

game = initialize_test_game(board_config)
x = 4
game.print_board()
while x < 80:
    
    start_pos = x
    print(start_pos)
    action = 1
    result = game.is_valid_move(game.board1, start_pos, action)
    game.update_board(start_pos, action)
    print(result)
    x += 9
game.print_board()   
i = 6




while i < 80:
    
    start_pos = i
    print(start_pos)
    action = -8
    result = game.is_valid_move(game.board1, start_pos, action)
    game.update_board(start_pos, action)
    print(result)
    i += 9
game.print_board()
