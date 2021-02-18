import json
import os

from src.Game import Game 
from src.Agent import Agent

with open(os.path.join(os.path.dirname(__file__), "./src/config/config.json")) as f:
    config = json.load(f)

agents = config["agents"]

while len(agents) > 1:
    pivotAgent = agents.pop()
    print(pivotAgent)

    for i in range(0, len(agents)):
        print(pivotAgent["name"] + ' vs. ' + agents[i]["name"])
        game = Game(
            config["board"][0], 
            config["board"][1], 
            config["winningSize"], 
            config["totalGames"],  
            Agent(1, [config["board"][0], config["board"][1]], config["winningSize"], pivotAgent["scoring"], pivotAgent["restrictMoves"]), 
            Agent(-1, [config["board"][0], config["board"][1]], config["winningSize"], agents[i]["scoring"], agents[i]["restrictMoves"]), 
            config["printMoves"])

        while game.totalGames > game.playedGames:
            game.playAgentMove()
        
        print(game.scores)
