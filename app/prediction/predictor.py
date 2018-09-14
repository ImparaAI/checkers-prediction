from game.game import Game
from model.model import Model
from model import input_builder

def predict(moves):
	game = build_game(moves)
	input_state = input_builder.build(game).input

	model = Model(input_state.shape(), 8 * game.board.height * game.board.width)
	model.predict(input_state);


	#montecarlo go and do you shit with these params


	return builder.build().predict(request)

def build_game(moves):
	game = Game()

	for move in moves:
		game.move(move)

	return game