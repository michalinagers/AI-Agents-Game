#connect 4 board, 7 by 6

board = [[" " for _ in range(7)] for _ in range(6)]

def print_board(board):
    for row in board: 
        print(" | ".join(row))
        print("-" * 25)

