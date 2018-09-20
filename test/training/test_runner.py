import unittest
from app.training.session.runner import Runner

from app.prediction.predictor import build_game

class test_runner(unittest.TestCase):

	def test(self):
		#game = build_game([[9, 14], [24, 19], [5, 9], [23, 18], [14, 23], [27, 18], [9, 14], [18, 9], [6, 13], [28, 24], [11, 15], [24, 20], [15, 24], [22, 17], [13, 22], [25, 18], [8, 11], [29, 25], [11, 16], [20, 11], [7, 16], [26, 23], [10, 14], [18, 9], [4, 8], [9, 6], [2, 9], [30, 26], [3, 7], [23, 19], [16, 23], [23, 30], [31, 26], [30, 23], [32, 28], [9, 14], [28, 19]])
		#print(game.is_over())
		#print(game.get_possible_moves())

		Runner().run()