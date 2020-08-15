# hangman
A well known game Hangman for two players. Guess the movie title.
1. Run hangman.py.
2. Run client.py for each player.

Game starts when two players connect to socket.
Both players are guessing same movie title. They have six lives in total.

First one to try to guess is chosen randomly. If his guess is correct, movie title contains given letter, than he continues guessing.
If his input is incorrect, other player is allowed to guess. 
If any player loses 6th life, game is over and both players lost the game.
If one player guesses all the letters, he is a winner.

Note: With minor changes in code, it can be used for multiple players.
