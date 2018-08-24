import unittest
from app.game.game import Game

class TestGameOver(unittest.TestCase):

	def test_new_game_not_over(self):
		self.assertEqual(Game().is_over(), False)