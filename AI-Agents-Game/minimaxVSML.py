from gameTreeVisualisation import create_game_tree
from gameBoard import print_board
from MLagent import hybrid_best_move, load_models
from minimaxAgent import best_move, check_winner, is_full, get_available_moves
from piechart import createPieChart
import matplotlib.pyplot as plt

nn_model, rf_model = load_models('connect_four_dataset.pkl')

def playgame_miniMaxVsMLagent():
    #game_history = [] #for storing the player's moves during the game
    board = [[" " for _ in range(7)] for _ in range(6)]  #6 rows, 7 columns

    print("Welcome to Connect 4! MiniMax (X) vs ML Agent (O).")
    print_board(board)

    while True:
        #minimax agent move
        col = best_move(board, ai_player="X", human_player="O")
        for row in reversed(range(6)):
            if board[row][col] == " ":
                board[row][col] = "X"
                #game_history.append(("MiniMax Agent", col))
                print(f"MiniMax Agent placed 'X' at ({row}, {col}).")
                break

        print_board(board)

        if check_winner(board, "X"):
            print("MiniMax Agent wins!")
            return "MiniMax Agent"

        if is_full(board):
            print("It's a draw!")
            return "Draw"

        #ML agent move
        row, col = hybrid_best_move(board, nn_model, rf_model)
        if board[row][col] == " ":
                board[row][col] = "O"
                #game_history.append(("ML Agent", col))
                print(f"ML Agent placed 'O' at ({row}, {col}).")
            

        print_board(board)

        if check_winner(board, "O"):
            print("ML Agent wins!")
            return "ML Agent"

        if is_full(board):
            print("It's a draw!")
            return "Draw"
        
        #create_game_tree(game_history)
        print("Game Over!")

def miniMaxVSMLGames(games=500):

    result = {"MiniMax Agent": 0, "ML Agent": 0, "Draw": 0}
    for _ in range(500):
        winner = playgame_miniMaxVsMLagent()
        if winner in result:
            result[winner] += 1
    print(f"Games played: {games}")
    print(f"MiniMax Agent won: {result['MiniMax Agent']} times")
    print(f"ML Agent won: {result['ML Agent']} times")
    print(f"Draws: {result['Draw']}")

if __name__ == "__main__":

    result_counts = miniMaxVSMLGames(games=500)

    counts = [result_counts['Mini-Max Agent'], result_counts['ML Agent'], result_counts['Draw']]

    fig = createPieChart(
        sizes=counts,
        labels=["Mini-Max Agent", "ML Agent", "Draws"],
        title="Mini-Max Agent vs ML Agent Results (500 Games)"
    )

    plt.savefig('MiniMaxVSML.png', bbox_inches='tight', dpi=300)
    plt.show()

