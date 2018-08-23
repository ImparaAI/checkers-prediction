import unittest
from app.game.game import Game

class TestGame(unittest.TestCase):

	def test_new_game_not_over(self):
		self.assertEqual(Game().is_over(), False)

	def test_possible_moves_for_only_positional_moves(self):
		game = Game()

		self.assertEqual(game.get_possible_moves(), [[9, 13], [9, 14], [10, 14], [10, 15], [11, 15], [11, 16], [12, 16]])
		self.assertEqual(game.move([9, 13]).get_possible_moves(), [[21, 17], [22, 17], [22, 18], [23, 18], [23, 19], [24, 19], [24, 20]])
		self.assertEqual(game.move([24, 19]).get_possible_moves(), [[5, 9], [6, 9], [13, 17], [10, 14], [10, 15], [11, 15], [11, 16], [12, 16]])
		self.assertEqual(game.move([6, 9]).get_possible_moves(), [[21, 17], [22, 17], [22, 18], [23, 18], [19, 15], [19, 16], [27, 24], [28, 24]])
		self.assertEqual(game.move([21, 17]).get_possible_moves(), [[1, 6], [2, 6], [9, 14], [10, 14], [10, 15], [11, 15], [11, 16], [12, 16]])