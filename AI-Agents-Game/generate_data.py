import random
import pickle
from minimaxAgent import best_move 
from tqdm import tqdm  #tqdm for progress bar

def get_next_available_row(board, col):
    for row in range(5, -1, -1):  #from bottom to top
        if board[row][col] == " ":
            return row
    return None

def check_winner(board, player):

    for row in range(6):
        for col in range(4):
            if all(board[row][col + i] == player for i in range(4)):
                return True
    for col in range(7):
        for row in range(3):
            if all(board[row + i][col] == player for i in range(4)):
                return True
    for row in range(3):
        for col in range(4):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True
    for row in range(3, 6):
        for col in range(4):
            if all(board[row - i][col + i] == player for i in range(4)):
                return True
    return False

#rule based agent
def rule_based_move(board, player):
    #rule 1 win
    for col in range(7):
        row = get_next_available_row(board, col)
        if row is not None:
            board[row][col] = player
            if check_winner(board, player):
                return col 
            board[row][col] = " "
    
    #rule 2 block opponent
    opponent = "O" if player == "X" else "X"
    for col in range(7):
        row = get_next_available_row(board, col)
        if row is not None:
            board[row][col] = opponent
            if check_winner(board, opponent):
                board[row][col] = " "  # Undo move
                return col  # Block the opponent
            board[row][col] = " "
    
    #rule 3 center column
    center_col = 3 
    if board[0][center_col] == " ":
        return center_col
    
    #rule 4 random move
    available_cols = [c for c in range(7) if board[0][c] == " "]
    return random.choice(available_cols)

#simulate a game for dataset generation
def simulate_game():
    board = [[" " for _ in range(7)] for _ in range(6)]
    player = "X"
    history = []
    
    while True:
        if player == "X":
            col = rule_based_move(board, "X")
        else:  
            col = best_move(board, ai_player="O", human_player="X")  
        
        row = get_next_available_row(board, col)
        if row is not None:
            board[row][col] = player
        
        #record the board state for the dataset training
        flat_board = [1 if c == "X" else -1 if c == "O" else 0 for row in board for c in row]
        history.append((flat_board, col, player))  #board state, move, and current player
        
        #checking for winner
        if check_winner(board, player):
            return history, player 
        if all(board[row][col] != " " for row in range(6) for col in range(7)): 
            return history, "Draw" 
        
        player = "O" if player == "X" else "X"

#generate dataset with a progress bar to see if the code is running
def generate_dataset(num_games=1000):
    all_games = []
    for _ in tqdm(range(num_games), desc="Generating games", unit="game"):  # Adding progress bar
        game_history, winner = simulate_game()
        all_games.append((game_history, winner))
    
    #saving the dataset
    with open("connect_four_dataset.pkl", "wb") as f:
        pickle.dump(all_games, f)
    print("Dataset generated and saved to connect_four_dataset.pkl")

#running the dataset generation with 1000 games
if __name__ == "__main__":
    generate_dataset(num_games=1000)
