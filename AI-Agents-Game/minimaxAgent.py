##add heuristic search to this agent
# minimax.py
import numpy as np
from gameTreeVisualisation import create_game_tree
from gameBoard import print_board


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
    return [col for col in range(7) if board[0][col] == " "]


def minimax(board, depth, max_depth, alpha, beta, is_maximizing, ai_player, human_player):
    if check_winner(board, ai_player):
        return 10 - depth
    elif check_winner(board, human_player):
        return depth - 10
    elif is_full(board) or depth == max_depth:  #stopping at max depth
        return 0


    #alpha-beta pruning
    if is_maximizing:
        max_eval = float('-inf')
        for col in get_available_moves(board):
            row = next(row for row in reversed(range(6)) if board[row][col] == " ")
            board[row][col] = ai_player
            eval = minimax(board, depth + 1, max_depth, alpha, beta, False, ai_player, human_player)
            board[row][col] = " "
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for col in get_available_moves(board):
            row = next(row for row in reversed(range(6)) if board[row][col] == " ")
            board[row][col] = human_player
            eval = minimax(board, depth + 1, max_depth, alpha, beta, True, ai_player, human_player)
            board[row][col] = " "
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval
   
#heuristic evaluation function as A* and misplaced tiles algorithm is not suitable for this game
#as it is not a pathfinding problem, we can use a heuristic evaluation function to evaluate the board state


def evaluate_board(self, board):
        """Heuristic function: Assigns a score to the board state."""
        score = 0


        #center column bonus
        center_col = board[:, board.shape[1] // 2]
        score += list(center_col).count(self.ai_player) * 3


        #checking horizontal lines
        for row in range(board.shape[0]):
            for col in range(board.shape[1] - 3):
                window = list(board[row, col:col+4])
                score += self.simple_window_score(window)


        #checking vertical lines
        for col in range(board.shape[1]):
            for row in range(board.shape[0] - 3):
                window = list(board[row:row+4, col])
                score += self.simple_window_score(window)


        return score
   
def simple_window_score(self, window):
        """Score a window of 4 cells."""
        score = 0
        if window.count(self.ai_player) == 4:
            score += 100
        elif window.count(self.ai_player) == 3 and window.count(" ") == 1:
            score += 5
        elif window.count(self.ai_player) == 2 and window.count(" ") == 2:
            score += 2
        if window.count(self.human_player) == 3 and window.count(" ") == 1:
            score -= 4
        return score
   
def best_move(board, ai_player, human_player, max_depth=2):
    best_val = float('-inf')
    best_col = None
   
    #iterative deepening loop, increase the depth from 1 to max_depth
    for depth in range(1, max_depth + 1):
        #print(f"Searching at depth {depth}...")
        for col in get_available_moves(board):
            row = next(row for row in reversed(range(6)) if board[row][col] == " ")
            board[row][col] = ai_player
            move_val = minimax(board, 0, depth, float('-inf'), float('inf'), False, ai_player, human_player)
            board[row][col] = " "
           
            #updating best move if this one is better
            if move_val > best_val:
                best_val = move_val
                best_col = col


    #returning the best column after iterative deepening
    return best_col if best_col is not None else get_available_moves(board)[0]

#human move function
def humanMove(board):
    while True:
        try:
            col = int(input("Enter your move (column number 0-6): "))
            if 0 <= col < 7:
                for row in reversed(range(6)):
                    if board[row][col] == " ":
                        board[row][col] = "X"
                        return col  #return the column
                print("Column is full! Try a different column.")
            else:
                print("Invalid column. Enter a number between 0 and 6.")
        except ValueError:
            print("Invalid input. Enter a number between 0 and 6.")

#creating a game tree
def is_gameEnd(board, ai_player, human_player):
    return check_winner(board, ai_player) or check_winner(board, human_player) or is_full(board)


def playgame_miniMaxAgent():
    game_history = []  #for storing moves for game tree visualization
    board = [[" " for _ in range(7)] for _ in range(6)]
    ai_player = "O"
    human_player = "X"
    turn = "human"
   
    while not is_full(board):
        print_board(board)
       
        if check_winner(board, human_player):
            print("You have won!")
            break


        if check_winner(board, ai_player):
            print("Mini Max Agent wins!")
            break


        if turn == "human":
            col = humanMove(board)
            for row in reversed(range(6)):
                if board[row][col] == "X":
                    game_history.append(("Human", col))
                    break
            turn = "AI"
        else:
            col = best_move(board, ai_player, human_player)
            if col is not None:
                row = next(row for row in reversed(range(6)) if board[row][col] == " ")
                print(f"Mini Max Agent placed 'O' at ({row}, {col}).")
                board[row][col] = ai_player
                game_history.append(("AI", col))
            turn = "human"


        if is_full(board):
            print("It's a tie!")
            break


    print_board(board)
    create_game_tree(game_history)  #display the game tree after the game ends
    print("Game Over!")





