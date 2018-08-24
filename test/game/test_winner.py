import unittest
from app.game.game import Game

import random

class TestWinner(unittest.TestCase):

	def setUp(self):
		self.game = Game()

	def test_player_1_wins(self):
		self.make_non_winning_moves([[11, 15], [21, 17], [8, 11], [25, 21], [4, 8], [29, 25], [12, 16], [22, 18], [15, 22], [22, 29], [30, 25], [29, 22], [22, 13], [23, 18],
			[8, 12], [26, 23], [16, 20], [31, 26], [3, 8], [24, 19], [10, 14], [21, 17], [13, 22], [22, 31], [31, 24], [24, 15], [15, 22], [32, 27], [9, 13], [23, 18],
			[14, 23], [23, 32], [28, 24]])

		self.move([20, 27]).expect(1)

	def test_player_2_wins(self):
		self.make_non_winning_moves([[10, 14], [22, 17], [9, 13], [17, 10], [6, 15], [23, 18], [15, 22], [25, 18], [13, 17], [21, 14], [5, 9], [14, 5], [1, 6], [5, 1],
			[11, 15], [1, 10], [10, 19], [12, 16], [19, 12], [7, 10], [26, 23], [10, 14], [18, 9], [3, 7], [12, 3], [3, 10], [2, 6], [9, 2], [4, 8], [2, 7], [8, 11]])

		self.move([7, 16]).expect(2)

	def test_draw_no_winner(self):
		self.game.move_limit = 15
		self.make_non_winning_moves([[9, 13], [22, 17], [13, 22], [26, 17], [10, 14], [17, 10], [7, 14], [23, 18], [14, 23], [27, 18], [12, 16], [18, 15], [11, 18],
			[25, 22], [18, 25]])

	def make_non_winning_moves(self, moves):
		for move in moves:
			self.move(move).expect(None)

	def move(self, move):
		self.game.move(move);
		return self

	def expect(self, value):
		self.assertIs(self.game.get_winner(), value);