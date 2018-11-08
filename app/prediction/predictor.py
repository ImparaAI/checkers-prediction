from app.player import Player
from checkers.game import Game
from app.model.checkers import model as checkers_model

def predict(moves, simulation_count = 5):
	game, prior_boards = initialize_game(moves)
	model = checkers_model.build()
	player = Player(game.whose_turn(), game, model, prior_boards)

	return player.simulate(simulation_count).get_next_move()

def initialize_game(moves):
	game = Game()
	boards = [game.board]

	for move in moves:
		game.move(move)
		boards.append(game.board)

	return game, boards