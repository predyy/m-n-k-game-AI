# Game

## Properties
| Property | Description |
| -------- | ----------- |
| board   | Board array, 0 - empty field, 1 - player one move, -1 - player two move |
| boardSize[width, height]   | Width and height of game board |
| playedGames   | Number of already played games |
| totalGames   | Number of games to be played in total |
| playerTurn   | 1 or -1, switching every turn |     
| agents   | Array of two agents playing current game |
| winningSize   | Size of winning combination |
| scores   | Scores of played games in format [playerOneWins, playerTwoWins] |
| endTurnPrint   | If true all played moves will be played |

## Gameplay
Game is played by first getting agent move `getAgentMove()`,  then playing it by calling `playMove()`, updating memory of agents by calling their methods `newMovePlayed()` then checking for win and switching turn in `endTurn()`.

## Win checking
We trust first agent to count combinations correctly and if one is greater than `winningSize` we consider game over.

## Creating new game after finish
New game is created as new object, agents memory is cleared by `forget()` method. All is done in driver code.

