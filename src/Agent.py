import random
import numpy

class Agent:
    def __init__(self, playerNumber, boardSize, winningSize, scoringArray, restrictMoves): 
        #Agent remembers best found move for every beggining postion he ever evaluated
        self.memory = {
            "lastBoardState": [0] * boardSize[0] * boardSize[1],
            "lastMovePlayed": [-1, -1], #x, y
            #To be counted as sequence it must be open atleast on one side e.g. -1,1,1,1,0 is three
            "lastBoardStateSequences": {
                "playerOne": [0] * (winningSize + 1),    #e.g. count of fours is on index 4
                "playerTwo": [0] * (winningSize + 1)
            }
        }
        self.playerNumber = playerNumber
        self.boardSize = boardSize       
        self.winningSize = winningSize 
        self.scoringArray = [0] + scoringArray
        self.restrictMoves = restrictMoves

    def forget(self):
        self.memory = {
            "lastBoardState": [0] * self.boardSize[0] * self.boardSize[1],
            "lastMovePlayed": [-1, -1],
            "lastBoardStateSequences": {
                "playerOne": [0] * (self.winningSize + 1),
                "playerTwo": [0] * (self.winningSize + 1)
            }
        }

    def getNextMove(self):
        if (self.memory["lastMovePlayed"] == [-1, -1]):
            return [random.randint(0,self.boardSize[0]-1), random.randint(0,self.boardSize[1]-1)]

        state = {
            "boardState": self.memory["lastBoardState"],
            "lastMove": self.memory["lastMovePlayed"],
            "sequences": (self.memory["lastBoardStateSequences"]["playerOne"], self.memory["lastBoardStateSequences"]["playerTwo"]),
        }
        
        move = self.minimax(state, 5, float("-inf"), float("inf"), True)
        return move[0]

    def newMovePlayed(self, boardState):
        for i in range(0, self.boardSize[0]*self.boardSize[1]):
            if boardState[i] != self.memory["lastBoardState"][i]:
                self.memory["lastMovePlayed"] = [i % self.boardSize[0], i // self.boardSize[1]]
                break

        newSquences = self.countSequences(self.memory["lastBoardStateSequences"]["playerOne"], self.memory["lastBoardStateSequences"]["playerTwo"], self.memory["lastBoardState"], boardState, self.memory["lastMovePlayed"])
        
        self.memory["lastBoardStateSequences"]["playerOne"] = newSquences[0]
        self.memory["lastBoardStateSequences"]["playerTwo"] = newSquences[1]
        self.memory["lastBoardState"] = boardState.copy()

    def countSequences(self, playerOneSequences, playerTwoSequences, boardStateOld, boardStateNew, move):
        #Sequence counting is done by first counting incident sequences on old board, subtracting 
        #them from total and then adding new sequences from new board.
        
        playerOne = playerOneSequences.copy()
        playerTwo = playerTwoSequences.copy()

        #Rows       
        oldRows = self.countRows(boardStateOld, move)
        newRows = self.countRows(boardStateNew, move)

        #Columns
        oldColumns = self.countColumns(boardStateOld, move)
        newColumns = self.countColumns(boardStateNew, move)

        #Down diagonal
        oldDownDiagonal = self.countDownDiagonal(boardStateOld, move)
        newDownDiagonal = self.countDownDiagonal(boardStateNew, move)

        #Up diagonal
        oldUpDiagonal = self.countUpDiagonal(boardStateOld, move)
        newUpDiagonal = self.countUpDiagonal(boardStateNew, move)

        for i in range(1, self.winningSize+1):
            playerOne[i] = playerOne[i] - oldRows[0][i] + newRows[0][i] - oldColumns[0][i] + newColumns[0][i] - oldUpDiagonal[0][i] + newUpDiagonal[0][i] - oldDownDiagonal[0][i] + newDownDiagonal[0][i]
            playerTwo[i] = playerTwo[i] - oldRows[1][i] + newRows[1][i] - oldColumns[1][i] + newColumns[1][i] - oldUpDiagonal[1][i] + newUpDiagonal[1][i] - oldDownDiagonal[1][i] + newDownDiagonal[1][i]

        return (playerOne, playerTwo)

    def countRows(self, boardState, move):
        playerOne = [0] * (self.winningSize + 1)
        playerTwo = [0] * (self.winningSize + 1)

        #Cylce iterates over all possible starting points
        counting = 0
        currentSequenceIsValid = False
        length = 0

        for i in range(move[1]*self.boardSize[0], move[1]*self.boardSize[0]+self.boardSize[0]):    
            if (boardState[i] != counting):
                if (length > self.winningSize):
                    length = self.winningSize
                
                if (counting == 0 or boardState[i] == 0):
                    #Sequence must start or end with empty space to be valid
                    currentSequenceIsValid = True
                if (counting == 1 and currentSequenceIsValid):
                    playerOne[length] += 1
                    currentSequenceIsValid = False
                if (counting == -1 and currentSequenceIsValid):                    
                    playerTwo[length] += 1
                    currentSequenceIsValid = False

                counting = boardState[i]
                length = 1
            else:
                counting = boardState[i]
                length += 1

        #Sequence could end on board end
        if (counting != 0 and currentSequenceIsValid):
            if (length > self.winningSize):
                length = self.winningSize
                
            if (counting == 1):
                playerOne[length] += 1
            else:
                playerTwo[length] += 1
        
        return(playerOne, playerTwo)

    def countColumns(self, boardState, move): 
        playerOne = [0] * (self.winningSize + 1)
        playerTwo = [0] * (self.winningSize + 1)

        #Cylce iterates over all possible starting points
        counting = 0
        currentSequenceIsValid = False
        length = 0

        for i in range(move[0], self.boardSize[0]*self.boardSize[1], self.boardSize[1]):            
            if (boardState[i] != counting):
                if (length > self.winningSize):
                    length = self.winningSize

                if (counting == 0 or boardState[i] == 0):
                    #Sequence must start or end with empty space to be valid
                    currentSequenceIsValid = True
                if (counting == 1 and currentSequenceIsValid):
                    playerOne[length] += 1
                    currentSequenceIsValid = False
                if (counting == -1 and currentSequenceIsValid):                    
                    playerTwo[length] += 1
                    currentSequenceIsValid = False

                counting = boardState[i]
                length = 1
            else:
                counting = boardState[i]
                length += 1

        #Sequence could end on board end
        if (counting != 0 and currentSequenceIsValid):
            if (length > self.winningSize):
                length = self.winningSize
                
            if (counting == 1):
                playerOne[length] += 1
            else:
                playerTwo[length] += 1
        
        return(playerOne, playerTwo)

    
    def countDownDiagonal(self, boardState, move): 
        playerOne = [0] * (self.winningSize + 1)
        playerTwo = [0] * (self.winningSize + 1)

        #Cylce iterates over all possible starting points
        counting = 0
        currentSequenceIsValid = False
        length = 0

        #Math magic works as follows:
        #First element on diagonal can be calculated from move by modulo length of step
        #Every step is length of row + 1
        for i in range((move[0]+(move[1]*self.boardSize[0]))%(self.boardSize[0]+1), self.boardSize[0]*self.boardSize[1], self.boardSize[0]+1):   
            if (boardState[i] != counting):
                if (length > self.winningSize):
                    length = self.winningSize
                
                if (counting == 0 or boardState[i] == 0):
                    #Sequence must start or end with empty space to be valid
                    currentSequenceIsValid = True
                if (counting == 1 and currentSequenceIsValid):
                    playerOne[length] += 1
                    currentSequenceIsValid = False
                if (counting == -1 and currentSequenceIsValid):                    
                    playerTwo[length] += 1
                    currentSequenceIsValid = False

                counting = boardState[i]
                length = 1
            else:
                counting = boardState[i]
                length += 1
            
            #Handle diagonal overflowing board by checking if we didn't skip a row by increasing index 
            if (i // self.boardSize[1] + 1 != ((i + self.boardSize[0] + 1) // self.boardSize[1])):
                break

        #Sequence could end on board end
        if (counting != 0 and currentSequenceIsValid):
            if (length > self.winningSize):
                length = self.winningSize
                
            if (counting == 1):
                playerOne[length] += 1
            else:
                playerTwo[length] += 1
        
        return(playerOne, playerTwo)

    def countUpDiagonal(self, boardState, move): 
        playerOne = [0] * (self.winningSize + 1)
        playerTwo = [0] * (self.winningSize + 1)

        #Cylce iterates over all possible starting points
        counting = 0
        currentSequenceIsValid = False
        length = 0

        #Math magic works as follows:
        #First element on diagonal can be calculated from move by modulo length of step
        #Every step is length of row - 1
        for i in range((move[0]+(move[1]*self.boardSize[0]))%(self.boardSize[0]-1), self.boardSize[0]*self.boardSize[1], self.boardSize[0]-1):   
            if (boardState[i] != counting):
                if (length > self.winningSize):
                    length = self.winningSize
                
                if (counting == 0 or boardState[i] == 0):
                    #Sequence must start or end with empty space to be valid
                    currentSequenceIsValid = True
                if (counting == 1 and currentSequenceIsValid):
                    playerOne[length] += 1
                    currentSequenceIsValid = False
                if (counting == -1 and currentSequenceIsValid):                    
                    playerTwo[length] += 1
                    currentSequenceIsValid = False

                counting = boardState[i]
                length = 1
            else:
                counting = boardState[i]
                length += 1
            
            #Handle diagonal overflowing board by checking if we didn't end on a same row by increasing index 
            if (i // self.boardSize[1] == ((i + self.boardSize[0] - 1) // self.boardSize[1])):
               break

        #Sequence could end on board end
        if (counting != 0 and currentSequenceIsValid):
            if (length > self.winningSize):
                length = self.winningSize
                
            if (counting == 1):
                playerOne[length] += 1
            else:
                playerTwo[length] += 1
        
        return(playerOne, playerTwo)

    def isMoveTooFarFromAction(self, board, move):
        #Move is considered too far if there is no other move in 2 wide circle
        parsedMove = move % self.boardSize[0], move // self.boardSize[1]
        
        #Search one sized cricle
        circle = [ 
                [2,2],  [1,2],  [0,2],  [-1,2], [-2,2],
                [2,1],  [1,1],  [0,1],  [-1,1], [-2,1],
                [2,0],  [1,0],          [-1,0], [-2,0],   
                [2,-1], [1,-1], [0,-1], [-1,-1],[-2,-1],
                [2,-2], [1,-2], [0,-2], [-1,-2],[-2,-2]
            ]

        for circleIndex in circle:
            if (parsedMove[0]+circleIndex[0] >= self.boardSize[0] or parsedMove[0]+circleIndex[0] < 0): continue
            if (parsedMove[1]+circleIndex[1] >= self.boardSize[1] or parsedMove[1]+circleIndex[1] < 0): continue

            if ((board[parsedMove[0]+circleIndex[0] + (parsedMove[1]+circleIndex[1])*self.boardSize[1]]) != 0):
                return False
        
        return True

    def generateNextMoves(self, state, player): 
        nextMoves = []
        nextStates = []

        for i in range(0, len(state["boardState"])):
            if (state["boardState"][i] == 0):
                if (not self.isMoveTooFarFromAction(state["boardState"], i)):
                    nextMoves.append(i)

        for i in range(0, len(nextMoves)):
            nextStates.append({
                "boardState": state["boardState"].copy(),
                "lastMove": [nextMoves[i] % self.boardSize[0], nextMoves[i] // self.boardSize[1]],
                "sequences": None,
                "evaluation": None
            })

            nextStates[i]["boardState"][nextMoves[i]] = player
            nextStates[i]["sequences"] = self.countSequences(state["sequences"][0], state["sequences"][1], state["boardState"], nextStates[i]["boardState"], nextStates[i]["lastMove"])
            nextStates[i]["evaluation"] = self.evaluate(nextStates[i])

        #Make job of alpha-beta easier by ordering from best/worst move and restricing number of checked moves
        sortedStates = sorted(nextStates, key=lambda k: k['evaluation'], reverse=(player == self.playerNumber))
        return( sortedStates[0:self.restrictMoves] )


    def evaluate(self, state):
        if (state["sequences"][0][self.winningSize] != 0):
            if (self.playerNumber == 1):
                return float("inf")
            return float("-inf")

        if (state["sequences"][1][self.winningSize] != 0):
            if (self.playerNumber == -1):
                return float("inf")
            return float("-inf")

        score = 0
        for i in range(1, self.winningSize):
            if self.playerNumber == 1:
                score += (state["sequences"][0][i] - state["sequences"][1][i]) * self.scoringArray[i]
            else:
                score += (state["sequences"][1][i] - state["sequences"][0][i]) * self.scoringArray[i]
        return score
    
    def isGameOver(self, state):
        if (state["sequences"][0][self.winningSize] != 0 or state["sequences"][1][self.winningSize] != 0):
            return True

        boardIsFull = True
        for i in range(len(state["boardState"])):
            if (state["boardState"][i] == 0):
                boardIsFull = False
                break
        
        return boardIsFull

    def printBoard(self, board):
        print("---------")
        for i in range(0, self.boardSize[1]):            
            printRow = []
            for j in range (0, self.boardSize[0]):
                if (board[i*self.boardSize[0]+j] == 1):
                    printRow.append("X")
                if (board[i*self.boardSize[0]+j] == -1):
                    printRow.append("O")
                if (board[i*self.boardSize[0]+j] == 0):
                    printRow.append("-")
            print(printRow)
        print("---------")

    def minimax(self, state, depth, alpha, beta, maximizing):
        if (depth == 0 or self.isGameOver(state)):
            return (state["lastMove"], self.evaluate(state))
        
        if maximizing:
            value = float("-inf")
            bestMove = None
            nextMoves = self.generateNextMoves(state, self.playerNumber)

            for move in nextMoves:
                node = self.minimax(move, depth-1, alpha, beta, False)
                #print(node[1], value)
                if (node[1] >= value):
                    value = node[1]
                    bestMove = node[0]
                alpha = max(alpha, value)

                if alpha >= beta:
                    break
            
            return (bestMove, value)
        else:
            value = float("inf")
            bestMove = None

            nextMoves = self.generateNextMoves(state, self.playerNumber*-1)

            for move in nextMoves:
                node = self.minimax(move, depth-1, alpha, beta, True)
                
                if (node[1] <= value):
                    value = node[1]
                    bestMove = node[0]

                beta = min(beta, value)
                if beta <= alpha:
                    break

            return (bestMove, value)           