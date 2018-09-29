A Python Flask app that uses unsupervised learning to train a neural network to learn how to play checkers (aka draughts).

This was built to work in conjunction with the [web app](https://github.com/ImparaAI/checkers-web) and can easily be run in a Kubernetes cluster [here](https://github.com/ImparaAI/checkers-kubernetes). This app receives requests from the web app to restart the training, predict a move, or analyze previous training sessions. A mysql database is used for organizing the sessions and a cron flask script is used to perform the training runs.

# Routes

## /predict
Method: `GET`

Input: `moves=[[int, int], [int, int], ...]`

Output: `[int, int]`

## /training/session
Method: `POST`

Input: `episodes=int, time_limit_in_seconds=int`

## /training/sessions
Method: `GET`

# Commands

All commands can be run from the app root. If you are running this in the docker container, you don't need to worry about these as they are handled automatically.

## Initialize database

```
flask database:initialize
```

This only needs to be run if the database is not initialized, otherwise nothing will happen. The docker start script runs this on container startup.

## Run the next training session

```
flask training_session:run
```

Runs the next available training session. If a session is currently training, this will do nothing. This is run on a per-minute cron job in the docker container.

# Assumptions

The rules used are those defined by [our checkers library](https://github.com/ImparaAI/checkers). Importantly, each piece movement is completely distinct, with chained captures taking place over multiple turns where the player turn stays the same.

# Training strategy

This app uses a [Monte Carlo tree search library](https://github.com/ImparaAI/monte-carlo-tree-search) that roughly follows the methods used by [AlphaGo Zero](https://www.nature.com/articles/nature24270.epdf?author_access_token=VJXbVjaSHxFoctQQ4p2k4tRgN0jAjWel9jnR3ZoTv0PVW4gB86EEpGqTRDtpIz-2rmo8-KG06gqVobU5NSCFeHILHcVFUeMsbvwS-lxjqQGg98faovwjxeTUgZAUMnRQ). In short, every time it's the AI's turn to move, it uses one neural net to reduce the number of moves it should consider and another to evaluate the expected value of any particular move as we traverse the tree of possible moves in future rounds. In Google's terminology these are called the "policy network" and the "value network" respectively.

Each training run starts the neural net over from scratch. By default, a training run lasts for 1000 games, but it's also possible to restrict this on time and number of games depending on the limitations of your machine.

## Neural network architecture

The neural net's job is to reduce the amount of digging for the Monte Carlo tree search algorithm. The network itself is structurally identical to the AlphaZero network with the exception of the inputs, the predicted outputs, and certain small details in the convolutional layers

### Input

The input to the neural net is a multidimensional numpy array that is `34 x 8 x 4` (depth x height x width), or `34` layers of `8 x 4` 2d arrays. The `8 x 4` is determined by the shape of the board. Ignoring the white spaces, each checkers board has 8 vertical spots and 4 horizontal spots. The `34` is made up like this:

- Layers **1-32** hold the state of the board's pieces for the last 8 moves. So layers **1-4** hold the board state for the most recent move, layers **5-8** hold the board state for the second most recent move, etc. Within a single move's board state, the first layer describes the position of the current player's non-king pieces, the second layer is for the current opponent's non-king pieces, the third is the current player's king pieces, and the fourth is the current opponent's king pieces. The distinction between the current player and the opponent is important as the neural net only ever makes predictions from the perspective of the current player.
- Layer **33** has all 0s if it's player 1's turn and all 1s if it's player 2's turn.
- Layer **34** has a binary representation of the current move count. If it's move 29, that would be represented as `11101` in binary. That is then converted into a numpy `8 x 4` array that looks like `[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 1], [1, 1, 0, 1]]`.

The end result is that every value in this multidimensional input is either a `1` or a `0` and it fully represents everything about the current state of the board and the 7 previous moves.

### Outputs

The neural net has two outputs:

- A float that represents the expected win value for the current player given the current board state. In the Monte Carlo tree search algorithm this is the `W` value for the node being evaluated.
- A flat list 256 elements long, each of which hold a float value between `0` and `1` representing a success probability for choosing that move. Each spot on the board gets 8 potential move positions representing the direction and the distance of the move. So positions `0-7` in this array are reserved for spot 1's potential moves:

- **0**: move 1 spot to the southeast
- **1**: move 1 spot to the southwest
- **2**: move 1 spot to the northeast
- **3**: move 1 spot to the northwest
- **4**: move 2 spots to the southeast
- **5**: move 2 spots to the southwest
- **6**: move 2 spots to the northeast
- **7**: move 2 spots to the northwest

This is repeated for all 32 positions on the board, for a total of 256 elements.

During training, the output values are `0` for all impossible moves and a value between `0` and `1` for all possible moves. The value is determined by the number of visits in the Monte Carlo tree search simulation relative to the other possible moves. When the Monte Carlo tree search is making decisions about which moves to populate as child nodes, it iterates over all possible moves and finds the probability values (`p`) for them from this output, which eliminates the need to drill down further for that child node as you might do in a non-NN MCTS algorithm.

### Differences with AlphaZero

By default, this app uses 75 convolution kernels (i.e. "neurons") per convolutional layer whereas AlphaZero uses 256. AlphaZero also uses 40 residual layers where this app uses 6. The reasons for this are:

- Checkers is inherently simpler than Chess or Go
- We expect training to work decently on a moderately powerful CPU, rather than necessarily on a GPU or TPU

It's worth keeping in mind that in neural nets finding the right number of "neurons" and residual layers is a bit of an art. There may indeed be a way of precisely quantifying the correlation between prediction accuracy and these hyperparameters for specific problems, but when this app was made it was not immediately obvious to us how to do it. Our method for choosing these numbers was a process of trial and error with a goal of minimizing them (for performance) while subjectively keeping a high enough prediction accuracy.

# Why checkers?

Since checkers is a much simpler game than go or chess, the solution space is drastically reduced, while not being so trivial that it can be easily brute-forced on a regular computer in a short amount of time (like tic-tac-toe). This app's training can be run on a relatively cheap machine and doesn't really require a GPU or TPU.

# Testing

Go to the app directory and run `python3 -m unittest discover` or just `test` if you're in the Docker container.