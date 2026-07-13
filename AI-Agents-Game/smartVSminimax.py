from gameBoard import print_board
from gameBoard import board
from gameTreeVisualisation import create_game_tree
from smartAgent import smart_agent 
from minimaxAgent import best_move 
from minimaxAgent import check_winner, is_full, get_available_moves
from piechart import createPieChart
import matplotlib.pyplot as plt


def playgame_smartVsMiniMaxAgent():

    board = [[" " for _ in range(7)] for _ in range(6)]  #6 rows, 7 columns
    game_history = []
    print("Welcome to Connect 4! Smart Agent (X) vs Mini-Max Agent (O).")
    print_board(board)

    while True:
        #smart agent move
        col = smart_agent(board)
        for row in reversed(range(6)):
            if board[row][col] == " ":
                board[row][col] = "X"
                game_history.append(("Smart Agent", col))
                print(f"Smart Agent placed 'X' at ({row}, {col}).")
                break

        print_board(board)

        if check_winner(board, "X"):
            print("Smart Agent wins!")

            return "Smart Agent"

        if is_full(board):
            print("It's a draw!")
            return "Draw"

        #mini-max agent move
        col = best_move(board, ai_player="O", human_player="X")
        for row in reversed(range(6)):
            if board[row][col] == " ":
                board[row][col] = "O"
                game_history.append(("Mini-Max", col))
                print(f"Mini-Max Agent placed 'O' at ({row}, {col}).")
                break

        print_board(board)

        if check_winner(board, "O"):
            print("Mini-Max Agent wins!")
            return "MiniMax Agent"

        if is_full(board):
            print("It's a draw!")
            return "Draw"    

        #create_game_tree(game_history)
        print("Game Over!")

def smartVSMiniMaxGames(games=500):
    result = {"Smart Agent": 0, "Mini-Max Agent": 0, "Draw": 0} 

    for _ in range(games):
        winner = playgame_smartVsMiniMaxAgent() 
        if winner in result:
            result[winner] += 1  
    
    print(f"Games played: {games}")
    print(f"Smart Agent won: {result['Smart Agent']} times")
    print(f"Mini-Max Agent won: {result['Mini-Max Agent']} times")
    print(f"Draws: {result['Draw']}")
    
    return result  

if __name__ == "__main__":

    result_counts = smartVSMiniMaxGames(games=500)

    counts = [result_counts['Smart Agent'], result_counts['Mini-Max Agent'], result_counts['Draw']]

    fig = createPieChart(
        sizes=counts,
        labels=["Smart Agent", "Mini-Max Agent", "Draws"],
        title="Smart Agent vs MiniMax Agent Results (500 Games)"
    )

    plt.savefig('SmartVsMiniMaxResults.png', bbox_inches='tight', dpi=300)
    plt.show()
