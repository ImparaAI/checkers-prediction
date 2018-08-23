import unittest
from app.game.game import Game

class TestGame(unittest.TestCase):

	def test_new_game_not_over(self):
		self.assertEqual(Game().is_over(), False)

	def test_possible_moves_new_game(self):
		self.assertEqual(Game().get_possible_moves(), [[9, 13], [9, 14], [10, 14], [10, 15], [11, 15], [11, 16], [12, 16]])