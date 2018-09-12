import unittest
from app.game.game import Game
from app.model.action_space import get_action

class test_first_player(unittest.TestCase):

	def setUp(self):
		self.game = Game()

	def test_planes(self):
		self.assertEqual(self.get_actual(0, 4, 1), [15, 19])
		self.assertEqual(self.get_actual(1, 4, 1), [15, 18])
		self.assertEqual(self.get_actual(2, 4, 1), [15, 11])
		self.assertEqual(self.get_actual(3, 4, 1), [15, 10])
		self.assertEqual(self.get_actual(4, 4, 1), [15, 24])
		self.assertEqual(self.get_actual(5, 4, 1), [15, 22])
		self.assertEqual(self.get_actual(6, 4, 1), [15, 8])
		self.assertEqual(self.get_actual(7, 4, 1), [15, 6])

	def test_starting_positions(self):
		self.assertEqual(self.get_actual(0, 1, 1), [27, 32])
		self.assertEqual(self.get_actual(0, 3, 3), [17, 22])
		self.assertEqual(self.get_actual(0, 7, 2), [2, 7])

	def get_actual(self, plane, row, column):
		index = self.get_action_index(plane, row, column)
		return get_action(index, self.game)

	def get_action_index(self, plane, row, column):
		return (plane * 32) + (row * 4) + column;