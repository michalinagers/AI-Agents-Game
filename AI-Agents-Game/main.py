from randomAgent import playgame_randomAgent
from smartAgent import playgame_smartAgent
#from randomVSrule import playgame_ruleBasedvsRandomAgent
from randomVSrule import randomVSruleGames
from minimaxAgent import playgame_miniMaxAgent
from MLagent import playgame_MLAgent
from minimaxVSML import playgame_miniMaxVsMLagent
from minimaxVSML import miniMaxVSMLGames
from smartVSminimax import playgame_smartVsMiniMaxAgent
from smartVSminimax import smartVSMiniMaxGames

#defining the main game menu
def gameMenu():
    print("Welcome to Connect 4 Game! Choose an option from the menu below to start your game.")
    print("1. Play Connect 4 against Random Agent")
    print("2. Play Connect 4 against Smart Agent")
    print("3. Play Connect 4 against Mini-Max Agent")
    print("4. Play Connect 4 against ML Agent")
    print("5. View a Connect 4 game where Random Agent plays against Smart Agent")
    print("6. View a Connect 4 game where Mini-Max Agent plays against ML Agent")
    print("7. View a Connect 4 game where Smart Agent plays against Mini-Max Agent")
    print("8. Exit the game")

gameMenu()

menuOption = int(input("Enter your game option: "))

while menuOption != 0:
    if menuOption == 1:
        print("Starting a game against Random Agent..")
        playgame_randomAgent()
    elif menuOption == 2:
        print("Starting a game against Smart Agent..")
        playgame_smartAgent()
    elif menuOption == 3:
        print("Starting a game against Mini-Max Agent..")
        playgame_miniMaxAgent()
    elif menuOption == 4:
        print("Starting a game against ML Agent..")
        playgame_MLAgent()
    elif menuOption == 5:
        print("Starting a game Smart Agent vs Mini-Max Agent..")
        smartVSMiniMaxGames()
    elif menuOption == 6:
        print("Starting a game Random Agent vs Smart Agent..")
        randomVSruleGames()
    elif menuOption == 7:
        print("Starting a game Mini-Max Agent vs ML Agent..")
        miniMaxVSMLGames()
    elif menuOption == 8:
        exit()
    else:
        print("Invalid input")

    gameMenu()
    menuOption = int(input("Enter your game option: "))