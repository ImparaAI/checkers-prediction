from model import builder
from game.game import Game

def predict(request):
	game = Game()

	return builder.build().predict(request)