A Python Flask app that uses unsupervised learning to train a neural network to learn how to play checkers (aka draughts).

There are two endpoints: `/train` and `/predict`. These can be used to retrain the AI and predict the best move for a given board state. If no training has yet occurred, the AI will predict a random move.

This was built to work in conjunction with the [web app](https://github.com/ImparaAI/checkers-web) and can easily be run in a Kubernetes cluster as defined [here](https://github.com/ImparaAI/checkers-kubernetes).

# Routes

## /train
Method: `POST`

Input: `episodes=int, time_limit_in_seconds=int`

## /predict
Method: `GET`

Input: `moves=[[int, int], [int, int], ...]`

Output: `[int, int]`

# Assumptions

The rules used are for competitive American checkers or English draughts. This means an 8x8 board with force captures and regular kings.

Each position on the board is numbered 1 to 32. Each move is represented as an array with two values: starting position and ending position. So if you're starting a new game, one of the available moves is `[9, 13]` for player 1. If there's a capture move, the ending position is the position the capturing piece will land on (i.e. two rows from its original row), which might look like `[13, 22]`.

Each piece movement is completely distinct, even if the move is part of a multiple capture series. In [Portable Draughts Notation](https://en.wikipedia.org/wiki/Portable_Draughts_Notation) mutli-capture series are usually represented by a `5-32` (for a particularly long series of jumps), but in certain situations there could be multiple pathways to achieve that final position. This app requires an explicit spelling out of each distinct move in the multi-capture series. The app will understand when it's still a player's turn because it's mid-multi-capture.

# Training strategy

This app uses a Monte Carlo tree search that roughly follows the methods used by [AlphaGo Zero](https://www.nature.com/articles/nature24270.epdf?author_access_token=VJXbVjaSHxFoctQQ4p2k4tRgN0jAjWel9jnR3ZoTv0PVW4gB86EEpGqTRDtpIz-2rmo8-KG06gqVobU5NSCFeHILHcVFUeMsbvwS-lxjqQGg98faovwjxeTUgZAUMnRQ). In short, every time it's the AI's turn to move, it uses one neural net to reduce the number of moves it should consider and another to evaluate the expected value of any particular move as we traverse the tree of possible moves in future rounds. In Google's terminology these are called the "policy network" and the "value network" respectively.

Each training run starts the neural net over from scratch. By default, a training run lasts for 1000 games, but it's also possible to restrict this on time and number of games depending on the limitations of your machine.

## Neural network architecture

Both neural nets (`policy` and `value`) have identical inputs:

```
the current board state as two arrays of 32 spots (one for each player) where a 1 is a regular piece and a 2 is a king
the board state for the previous 8 moves
something about whose turn it is
```

# Why checkers?

Since checkers is a much simpler game than go or chess, the solution space is drastically reduced, while not being so trivial that it can be easily brute-forced on a regular computer in a short amount of time (like tic-tac-toe). This app's training can be run on a relatively cheap machine and doesn't really require a GPU or TPU.