#defining the random agent 
import random
from gameBoard import print_board
from gameBoard import board
from gameTreeVisualisation import create_game_tree

def check_winner(board, player):

    #check horizontal
    for row in range(6):
      for col in range(4):
        if all(board[row][col + i] == player for i in range(4)):
            return True
    
    #check vertical
    for col in range(7):
      for row in range(3):
        if all(board[row + i][col] == player for i in range(4)):
            return True
        
    #check diagonal \
    for row in range(3):
       for col in range(4):
          if all(board[row + i][col + i] == player for i in range(4)):
             return True
          
    #check diagonal /
    for row in range(3, 6):
        for col in range(4):
            if all(board[row - i][col + i] == player for i in range(4)):
                return True
    
    return False

def random_agent_move(board):
  empty_cells = [(row,col) for row in range(6) for col in range(7) if board[row][col] == " "]
  return random.choice(empty_cells)

def is_full(board):

    return all(board[row][col] != " " for row in range(6) for col in range(7))

def get_available_moves(board):

  available = False

  if board == [[" " for _ in range(6)] for _ in range(7)]:
    return available == True
  else:
    return available == False
  
def playgame_randomAgent():
    board = [[" " for _ in range(7)] for _ in range(6)]  #6 rows, 7 columns
    game_history = [] #for storing the player's moves during the game
    print("Welcome to Connect 4! You are 'X' and the Random Agent is 'O'.")
    print_board(board)

    while True: 
        while True:
            try:
                col = int(input("Enter your move (column number 0-6): "))
                if 0 <= col < 7:
                    #finding the lowest possible row in the given column
                    for row in reversed(range(6)):
                        if board[row][col] == " ":
                            game_history.append(("Human", col))
                            board[row][col] = "X"
                            break
                    else:
                        print("Column is full! Try a different column.")
                        continue
                    break
                else:
                    print("Invalid column. Enter a number between 0 and 6.")
            except ValueError:
                print("Invalid input. Enter a number between 0 and 6.")

        print_board(board)

        if check_winner(board, "X"):
            print("Congratulations! You win!")
            break 

        if is_full(board):
            print("It's a draw!")
            break 

        while True:
            col = random.randint(0, 6)
            for row in reversed(range(6)):
                if board[row][col] == " ":
                    board[row][col] = "O"
                    game_history.append(("Random Agent", col))
                    print(f"Random Agent placed 'O' at ({row}, {col}).")
                    break
            else:
                continue
            break

        print_board(board)
        create_game_tree(game_history)

        if check_winner(board, "O"):
            print("Random Agent wins! Better luck next time.")
            break 

        #checking for a draw
        if is_full(board):
            print("It's a draw!")
            break

