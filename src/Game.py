class Game:
    def __init__(self, boardSizeX, boardSizeY, winningSize, totalGames, agent1, agent2, print):
            self.board = [0] * boardSizeX * boardSizeY
            self.boardSize = [boardSizeX, boardSizeY]
            self.playedGames = 0
            self.totalGames = totalGames
            self.playerTurn = 1
            self.agents = [agent1, agent2]
            self.winningSize = winningSize
            self.scores = [0, 0]
            self.endTurnPrint = print
            


    def playAgentMove(self):
        move = self.getAgentMove()
        self.playMove(move[0], move[1])

    def getAgentMove(self):
        if (self.playerTurn == 1):
            return self.agents[0].getNextMove()
        return self.agents[1].getNextMove()

    def playMove(self, x, y):
        if (self.board[y*self.boardSize[1] + x] == 0):
            self.board[y*self.boardSize[1] + x] = self.playerTurn

            for i in range(0, len(self.agents)):
                self.agents[i].newMovePlayed(self.board)
            if (self.print):
                self.print()
            self.endTurn()

    def endTurn(self):
        self.checkForWin()
        self.playerTurn = -1 * self.playerTurn

    def handleWin(self, playerWin):        
        self.playedGames += 1
        if (playerWin == 1):
            self.scores[0] += 1
        if (playerWin == -1):
            self.scores[1] += 1

        #print(playerWin)
        if (self.playedGames < self.totalGames):
            self.board = [0] * self.boardSize[0] * self.boardSize[1]
            self.playerTurn = 1

            self.agents[0].forget()
            self.agents[1].forget()
        else:
            print("Played " + str(self.playedGames) + " games, with scores: " + str(self.scores[0]) + ":" + str(self.scores[1]) )


    def checkForWin(self):
        #We trust agent in order to save time checking board, this could be handled by "referee" agent
        if (self.agents[0].memory["lastBoardStateSequences"]["playerOne"][self.winningSize] >= 1):
            self.handleWin(1)
            return

        if (self.agents[0].memory["lastBoardStateSequences"]["playerTwo"][self.winningSize] >= 1):
            self.handleWin(-1)
            return

        boardIsFull = True
        for i in range(len(self.board)):
            if (self.board[i] == 0):
                boardIsFull = False
                break

        if (boardIsFull):
            self.handleWin(0)

    def print(self):
        print("---------")
        for i in range(0, self.boardSize[1]):            
            printRow = []
            for j in range (0, self.boardSize[0]):
                if (self.board[i*self.boardSize[0]+j] == 1):
                    printRow.append("X")
                if (self.board[i*self.boardSize[0]+j] == -1):
                    printRow.append("O")
                if (self.board[i*self.boardSize[0]+j] == 0):
                    printRow.append("-")
            print(printRow)
        print("---------")
