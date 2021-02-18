# Agent
Agent class.

## Properties
| Property | Description |
| -------- | ----------- |
| memory   | Dictionary of information about game state |
| memory["lastBoardState"]   | Last saved board state |
| memory["lastMovePlayed"]   | Last saved move |
| memory["lastBoardStateSequences"]   | Combinations of every player |
| playerNumber   | 1 or -1 depending on player number |     
| boardSize   | Size of board [width, height] |
| winningSize   | Size of winning combination |
| scoringArray   | Array of scores for every combination |
| restricMoves   | Number of best move explered |

## Updating game state
Game state is updated by Game object by calling function `newMovePlayed()`. When game is finished and not all games were played, new game is created and agents game memory is reset by calling `forget()`.

## Get move
`generateNextMoves()`

Called by game when it requires next move. Finding optimal move is done by minimax with alpha-beta pruning. If no move was played yet, random move will be returned.

## Move generation
`generateNextMoves()`

Move generation is done by taking all empty squares, not too far form already played moves (2-wide circle) and ordered by evaluation function to explore only specified amount of most promising moves.

## Move evaluation

`evaluate()`

Score is assigned for every combination and counted on board based on scoring array. Combination of length `i` is awarded score of `self.scoringArray[i]`.


## Combination counting

`countSequences()`

Agent keeps all combiation currently present in board and updates count after every move played. This is done by checking only rows, columns and diagonals incidental with move played.