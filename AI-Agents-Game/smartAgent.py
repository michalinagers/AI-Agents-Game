from gameBoard import board
from gameBoard import print_board
import random
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

def is_full(board):

    return all(board[row][col] != " " for row in range(6) for col in range(7))

def get_available_moves(board):
    moves = []
    for col in range(7):
        for row in reversed(range(6)):
            if board[row][col] == " ":
                moves.append((row, col))
                break
    return moves

def smart_agent(board):
  empty_cells = [(row,col) for row in range(6) for col in range(7) if board[row][col] == " "]
  #1 win if possible
  for row, col in get_available_moves(board):
    board[row][col] = "0"
    if check_winner(board, "0"):
      board[row][col] = " "
    return col

  #2 block opponent's win
  for row, col in get_available_moves(board):
    board[row][col] = "X"
    if check_winner(board, "X"):
      board[row][col] = "0"
      return col
    board[row][col] = " "

    
  #3 take center if possible 
  if board[5][3] == " ":
     return 3
    
  #4 take a corner if possible
  corners = [(0,0), (0,2), (2,0), (2,2)]
  random.shuffle(corners)
  for row, col in corners:
        if board[row][col] == " ":
            return col
        
  #5 random move
  available_columns = [col for col in range(7) if board[0][col] == " "]
  return random.choice(empty_cells)


def playgame_smartAgent():
    board = [[" " for _ in range(7)] for _ in range(6)]  #6 rows, 7 columns
    game_history = [] #for storing the player's moves during the game
    print("Welcome to Connect 4! You are 'X' and Smart Agent is 'O'.")
    print_board(board)

    while True: 
        while True:
            try:
                col = int(input("Enter your move (column number 0-6): "))
                if 0 <= col < 7:
                    #finding the lowest possible row in the given column
                    for row in reversed(range(6)):
                        game_history.append(("Human", col))
                        if board[row][col] == " ":
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
                    game_history.append(("Smart Agent", col))
                    print(f"Smart Agent placed 'O' at ({row}, {col}).")
                    break
            else:
                continue
            break

        print_board(board)
        create_game_tree(game_history)

        if check_winner(board, "O"):
            print("Smart Agent wins! Better luck next time.")
            break 

        #checking for a draw
        if is_full(board):
            print("It's a draw!")
            break

