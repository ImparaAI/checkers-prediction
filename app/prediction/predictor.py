from app.player import Player
from checkers.game import Game
from app.model.checkers import model as checkers_model

def predict(moves):
	game, prior_boards = initialize_game(moves)

	if game.is_over():
		raise ValueError('The game is already over.')

	possible_moves = game.get_possible_moves()

	if len(possible_moves) == 1:
		return possible_moves[0]

	model = checkers_model.build()
	player = Player(game.whose_turn(), game, model, prior_boards)

	return player.simulate(10).get_next_move()

def initialize_game(moves):
	game = Game()
	boards = [game.board]

	for move in moves:
		game.move(move)
		boards.append(game.board)

	return game, boards