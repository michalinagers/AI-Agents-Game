from gameBoard import board
from gameBoard import print_board
import random
from piechart import createPieChart
import matplotlib.pyplot as plt

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

  
def random_agent_move(board):
    available_moves = get_available_moves(board)
    return random.choice(available_moves)

def randomVSruleGames(games=500):

    result = {"Random Agent": 0, "Smart Agent": 0, "Draw": 0}
    for _ in range(500):
        winner = playgame_ruleBasedvsRandomAgent()
        if winner in result:
            result[winner] += 1
    print(f"Games played: {games}")
    print(f"Random Agent won: {result['Random Agent']} times")
    print(f"Smart Agent won: {result['Smart Agent']} times")
    print(f"Draws: {result['Draw']}")


def rule_based_agent(board):

    #win if possible
    for col in get_available_moves(board):
        for row in reversed(range(6)):  #places the drop in the lowest possible place in the board
            if board[row][col] == " ":
                board[row][col] = "O"
                if check_winner(board, "O"):
                    board[row][col] = " "  #reset board after checking
                    return col
                board[row][col] = " "  #reset board
                break

    #block opponent's win
    for col in get_available_moves(board):
        for row in reversed(range(6)):
            if board[row][col] == " ":
                board[row][col] = "X"
                if check_winner(board, "X"):
                    board[row][col] = " "
                    return col
                board[row][col] = " " 
                break

    #take center if available
    if board[0][3] == " ":
        return 3

    #take a corner if possible
    for col in [0, 6]: 
        if board[0][col] == " ":
            return col

    #choose a random move
    return random.choice(get_available_moves(board))


def playgame_ruleBasedvsRandomAgent():
    board = [[" " for _ in range(7)] for _ in range(6)]  #6 rows, 7 columns

    print("Welcome to Connect 4! Random Agent (X) vs Smart Agent (O).")
    print_board(board)

    while True:
        #random agent move
        col = random_agent_move(board)
        for row in reversed(range(6)):
            if board[row][col] == " ":
                board[row][col] = "X"
                print(f"Random Agent placed 'X' at ({row}, {col}).")
                break

        print_board(board)

        if check_winner(board, "X"):
            print("Random Agent wins!")
            return "Random Agent"

        if is_full(board):
            print("It's a draw!")
            return "Draw"

        #rule-based agent move
        col = rule_based_agent(board)
        for row in reversed(range(6)):
            if board[row][col] == " ":
                board[row][col] = "O"
                print(f"Smart Agent placed 'O' at ({row}, {col}).")
                break

        print_board(board)

        if check_winner(board, "O"):
            print("Smart Agent wins!")
            return "Smart Agent"

        if is_full(board):
            print("It's a draw!")
            return "Draw"

#gamesWinner(500)

if __name__ == "__main__":

    result_counts = randomVSruleGames(games=500)

    counts = [result_counts['Random Agent'], result_counts['Rule-Based Agent'], result_counts['Draw']]

    fig = createPieChart(
        sizes=counts,
        labels=["Random Agent", "Smart Agent", "Draws"],
        title="Random Agent vs Smart Agent Results (500 Games)"
    )

    plt.savefig('RandomVSsmartAgent.png', bbox_inches='tight', dpi=300)
    plt.show()
