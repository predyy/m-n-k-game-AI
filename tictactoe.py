from src.Game import Game 
from src.Agent import Agent

game = Game(10, 10, 5, 10,  Agent(1, [10,10], 5, [-1, 2, 100, 10000], 10), Agent(-1, [10,10], 5, [1000, 100, 10, 100000], 10), True)

while game.totalGames > game.playedGames:
    game.playAgentMove()
    #for i in range(0, len(game.agents)):
        #game.agents[i].newMovePlayed(game.board)
        #print(game.agents[i].memory)    

    #game.print()