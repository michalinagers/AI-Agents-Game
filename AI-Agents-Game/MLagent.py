import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle
from tqdm import tqdm

def train_nn_model(X_train, y_train, model, epochs=10, batch_size=64):
    print("Training neural network model")
    history = model.fit(
        X_train, y_train,
        epochs=epochs,
        batch_size=batch_size,
        validation_split=0.2,
        verbose=1,
        
    )
    print("Neural network training finished")
    return model

#checking if the board is full
def is_full(board):
    return all(board[row][col] != " " for row in range(6) for col in range(7))

#getting the next available row in a column
def get_available_moves(board):
    return [col for col in range(7) if board[0][col] == " "]

#checking the winner
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

#function for human move
def humanMove(board):
    while True:
        try:
            col = int(input("Enter your move (0-6): "))
            if 0 <= col < 7 and board[0][col] == " ":
                for row in reversed(range(6)):
                    if board[row][col] == " ":
                        board[row][col] = "X"
                        return
            else:
                print("Invalid or full column. Try again.")
        except ValueError:
            print("Please enter a number between 0 and 6.")

#function to print the board
def print_board(board):
    print("\n" + "-" * 29)
    for row in board:
        print("| " + " | ".join(cell if cell != " " else " " for cell in row) + " |")
        print("-" * 29)
    print("  0   1   2   3   4   5   6  ")  # Column numbers

#creating the neural network model
def create_nn_model():
    nn_model = keras.Sequential([
        keras.layers.Input(shape=(6, 7)), #6 rows, 7 columns
        keras.layers.Flatten(),
        keras.layers.Dense(128, activation='relu'), #128 rather than 64 neurons for indepth learning
        keras.layers.Dense(128, activation='relu'), #128 neurons for indepth learning
        keras.layers.Dense(7, activation='softmax')  #7 as there are 7 columns
    ])
    nn_model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return nn_model

#function to load the random forest model
def load_rf_model():
    try:
        with open('connect_four_rf_model.pkl', 'rb') as f:
            rf_model = pickle.load(f)
            print("Loaded existing Random Forest model")
            return rf_model
    except FileNotFoundError:
        print("Training new Random Forest model...")
        
        #creating training data if no dataset is available
        #to ensure the RF model always works
        print("Creating training data...")
        training_data = []
        
        #generating patterns
        for _ in range(1000):
            board = [[" " for _ in range(7)] for _ in range(6)]
            #filled with random moves
            for _ in range(np.random.randint(5, 20)):
                col = np.random.randint(0, 7)
                for row in reversed(range(6)):
                    if board[row][col] == " ":
                        board[row][col] = np.random.choice(["X", "O"])
                        break
            
            #flattening the board
            flat = [1 if c == 'X' else -1 if c == 'O' else 0 for row in board for c in row]
            
            #checking for winning patterns
            #assuming X is the human player and O is the ML agent
            has_x_win = check_winner(board, "X")
            has_o_win = check_winner(board, "O")
            
            if has_o_win:
                outcome = 1  #win for O (ML agent)
            elif has_x_win:
                outcome = -1  #lose for O (ML agent)
            else:
                outcome = 0  #draw
                
            training_data.append((flat, outcome))
        
        print(f"Generated {len(training_data)} training samples")
        
        X = np.array([d[0] for d in training_data])
        y = np.array([d[1] for d in training_data])
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        rf_model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
        rf_model.fit(X_train, y_train)
        
        y_pred = rf_model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Random Forest model accuracy on training data: {accuracy:.2f}")
        
        with open('connect_four_rf_model.pkl', 'wb') as f:
            pickle.dump(rf_model, f)
            
        return rf_model

#function to get the best move using hybrid approach 
#combining neural network and random forest
def hybrid_best_move(board, nn_model, rf_model, top_n=3):
    available_moves = get_available_moves(board)
    if not available_moves:
        return None, None
    
    #if only one move is available, make it
    if len(available_moves) == 1:
        move = available_moves[0]
        for row in reversed(range(6)):
            if board[row][move] == " ":
                board[row][move] = "O"
                return row, move
    
    #checking for winning moves
    for move in available_moves:
        temp_board = [row[:] for row in board]
        for row in reversed(range(6)):
            if temp_board[row][move] == " ":
                temp_board[row][move] = "O"
                if check_winner(temp_board, "O"):
                    board[row][move] = "O"
                    return row, move
                break
    
    #checking for opponent's winning moves
    for move in available_moves:
        temp_board = [row[:] for row in board]
        for row in reversed(range(6)):
            if temp_board[row][move] == " ":
                temp_board[row][move] = "X"  #check opponent's move
                if check_winner(temp_board, "X"):
                    board[row][move] = "O"  #block opponent
                    return row, move
                break
    
    #to store RF scores by move
    rf_scores_dict = {}
    
    try:
        #calculating RF scores for all available moves
        for move in available_moves:
            temp_board = [row[:] for row in board]
            
            for row in reversed(range(6)):
                if temp_board[row][move] == " ":
                    temp_board[row][move] = "O"
                    break
            
            #flattening the board for RF model
            temp_array = np.array([[1 if c == "X" else -1 if c == "O" else 0 for c in r] for r in temp_board])
            temp_flat = temp_array.flatten()
            
            #getting RF prediction
            try:
                probs = rf_model.predict_proba(temp_flat.reshape(1, -1))[0]
                #win prob - loss prob
                if len(probs) >= 3:
                    rf_score = probs[2] - probs[0] 
                else:
                    rf_score = 0.5  #default middle score if prediction fails
            except:
                rf_score = 0.5 
                
            rf_scores_dict[move] = rf_score
        
        #getting top N moves based on RF scores
        sorted_moves = sorted(available_moves, key=lambda m: rf_scores_dict[m], reverse=True)
        top_moves = sorted_moves[:min(top_n, len(sorted_moves))]
        
    except Exception as e:
        print(f"RF prediction error: {str(e)}")
        top_moves = available_moves
        rf_scores_dict = {move: 0.5 for move in available_moves} 
    
    #center column preference
    empty_count = sum(1 for row in board for cell in row if cell == " ")
    if empty_count >= 30 and 3 in available_moves:  #iff early game and center column is available
        center_weight = 0.2  #prefer center column in early game
    else:
        center_weight = 0.0
    
    best_score = -float('inf')
    best_col = None
    best_row = None
    
    #processing moves using neural network
    for move in top_moves:
        temp_board = [row[:] for row in board]
        
        #looking for row where piece will land
        for row in reversed(range(6)):
            if temp_board[row][move] == " ":
                temp_board[row][move] = "O"
                temp_row = row
                break
        
        #preparing input for neural network
        temp_array = np.array([[1 if c == "X" else -1 if c == "O" else 0 for c in r] for r in temp_board])
        
        #neural network prediction
        try:
            nn_scores = nn_model.predict(temp_array.reshape(1, 6, 7), verbose=0)[0]
            nn_score = nn_scores[move] 
        except:
            nn_score = 0.5 
        
        center_bonus = center_weight if move == 3 else 0
        
        #combining scores of RF and NN
        #using weights to balance the influence of each model
        combined_score = 0.7 * nn_score + 0.3 * rf_scores_dict[move] + center_bonus
        
        #adding a small random factor
        combined_score += np.random.uniform(0, 0.05)
        
        if combined_score > best_score:
            best_score = combined_score
            best_col = move
            best_row = temp_row
    
    #if no valid move was found
    if best_col is None:
        best_col = available_moves[0]
        for row in reversed(range(6)):
            if board[row][best_col] == " ":
                best_row = row
                break
    
    board[best_row][best_col] = "O"
    return best_row, best_col


def playgame_MLAgent(nn_model, rf_model):
    board = [[" " for _ in range(7)] for _ in range(6)]
    game_history = []  # for storing the player's moves during the game
    print("Welcome to Connect 4! You are 'X' and the ML Agent is 'O'.")
    turn = "human"

    while not is_full(board):
        print_board(board)

        if check_winner(board, "X"):
            print("You have won!")
            return
        if check_winner(board, "O"):
            print("ML Agent wins!")
            return

        if turn == "human":
            humanMove(board)
            game_history.append(("Human", board))
            turn = "AI"
        else:
            print("AI is thinking...")
            hybrid_best_move(board, nn_model, rf_model)
            game_history.append(("ML Agent", board))
            turn = "human"

    print_board(board)
    print("It's a tie!")


def load_models(dataset_path):
    with open(dataset_path, 'rb') as f:
        all_games = pickle.load(f)
    
    X = []  # Board states
    y = []  # Move labels (column 0–6)
    
    for game_history, winner in all_games:
        for flat_board, col, player in game_history:
            if player == "O":  # Only use ML Agent’s moves
                X.append(flat_board)
                y.append(col)
    
    X = np.array(X).reshape(-1, 6, 7)  # Reshape to (samples, 6, 7)
    y = keras.utils.to_categorical(y, num_classes=7)  # One-hot encode columns
    
    return X, y

try:
    X_nn, y_nn = load_models('connect_four_dataset.pkl')
    X_train, X_test, y_train, y_test = train_test_split(X_nn, y_nn, test_size=0.2, random_state=42)
    
    nn_model = create_nn_model()
    nn_model = train_nn_model(X_train, y_train, nn_model, epochs=500)
    
    # Evaluate the model to build compiled metrics
    test_loss, test_accuracy = nn_model.evaluate(X_test, y_test, verbose=0)
    print(f"Neural network test accuracy: {test_accuracy:.2f}")
    
    nn_model.save('nn_model.h5')
    print("Neural network model trained and saved!")
except FileNotFoundError:
    print("Dataset not found.")


if __name__ == "__main__":
    try:
        #loading both models
        nn_model, rf_model = load_models('connect_four_dataset.pkl')

        #starting game
        print("\nStarting Connect-4 game!")
        print("You are X, the AI is O")
        print("Columns are numbered 0-6 from left to right")
        playgame_MLAgent(nn_model, rf_model)
        
    except Exception as e:
        print(f"Error: {str(e)}")
        print("Exiting game")