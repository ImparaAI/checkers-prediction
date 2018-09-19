from app.player import Player
from checkers.game import Game
from app.model.checkers import model as checkers_model

def predict(moves, simulation_count = 5):
	game = build_game(moves)
	model = checkers_model.build()
	player = Player(game.whose_turn(), game, model)

	return player.simulate(simulation_count).get_next_move()

def build_game(moves):
	game = Game()

	for move in moves:
		game.move(move)

	return game