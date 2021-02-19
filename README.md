# (m,n,k)-game AI with configurable strategy

## (m,n,k)-game
An m,n,k-game is an abstract board game in which two players take turns in placing a stone of their color on an m×n board, 
the winner being the player who first gets k stones of their own color in a row, horizontally, vertically, or diagonally.

Thus, tic-tac-toe is the 3,3,3-game and free-style gomoku is the 15,15,5-game. 
An m,n,k-game is also called a k-in-a-row game on an m×n board.

**In program we consider every combination >= k winning.**

## How to use
Run:

`python tictactoe.py`

## Cofiguration
All cofiguration is provided in config.json.
| Property | Type | Description | 
| -------- | ---- | ----------- |
| board[width, height] | List[int] |  Size of the gameboard |
| winningSize | int | Size of winning combination |
| totalGames | int | Number of games to be played between every pair of agents |
| agents | Array[Object] | Definition of agents |
| agents[name] | String | Name of agent |
| agents[scoring] | Array[int] | Scoring of combitation explained below |
| agents[restricMoves] | Array[int] | Number of best moves to be explored on every tree level |
| printMoves | bool | If true, moves will be printed as games are played|

### Heuristic scoring
Scoring is represented by array of integers. Array must be size of `winningSize-1`. Item at index `i` represents score for open combination of size `i` in any direction. Combination is consirdered open when it can be extended atleast on one end.

Scores can be negative. Combinations are form every point in every direction. First move is chosen randomly.

**Example:**

`[1, 10, 100, 1000]`

At maximum depth and when deciding if postion is worth exploring, heuristic function will award 1 point for every open one, 10 for every two, 100 for three, 1000 for 4.

## Some results
10 games played on 15x15 board

```
    "agents": [
        {"name": "Simple", "scoring": [1, 10, 100, 1000], "restrictMoves": 5},
        {"name": "Spread", "scoring": [1000, 10, 10, 10], "restrictMoves": 5},
        {"name": "Cluster", "scoring": [-1000, 10, 10, 10], "restrictMoves": 5},
        {"name": "Base", "scoring": [0, 0, 0, 0], "restrictMoves": 5}
    ]
```

|     -      | Base | Simple | Spread | Cluster | 
|   ---      | ---  | ------ | ------ | ------- | 
| **Base**      | - | 5:5:0 | 8:2:0 | 2:8:0 |
| **Simple**    | 5:5:0 | - | 4:6:0 | 5:5:0 | 
| **Spread**    | 2:8:0 | 6:4:0 | - | 2:8:0 | 
| **Cluster**   | 8:2:0 | 5:5:0 | 8:2:0 | - | 