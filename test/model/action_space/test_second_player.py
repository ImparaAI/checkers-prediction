import unittest
from checkers.game import Game
from app.model.action_space import get_action

class test_second_player(unittest.TestCase):

	def setUp(self):
		self.game = Game()
		self.game.move([9, 13])

	def test_planes(self):
		self.assertEqual(self.get_actual(0, 4, 1), [18, 14])
		self.assertEqual(self.get_actual(1, 4, 1), [18, 15])
		self.assertEqual(self.get_actual(2, 4, 1), [18, 22])
		self.assertEqual(self.get_actual(3, 4, 1), [18, 23])
		self.assertEqual(self.get_actual(4, 4, 1), [18, 9])
		self.assertEqual(self.get_actual(5, 4, 1), [18, 11])
		self.assertEqual(self.get_actual(6, 4, 1), [18, 25])
		self.assertEqual(self.get_actual(7, 4, 1), [18, 27])

	def test_starting_positions(self):
		self.assertEqual(self.get_actual(0, 1, 1), [6, 1])
		self.assertEqual(self.get_actual(0, 3, 3), [16, 11])
		self.assertEqual(self.get_actual(0, 7, 2), [31, 26])

	def get_actual(self, plane, row, column):
		index = self.get_action_index(plane, row, column)
		return get_action(index, self.game)

	def get_action_index(self, plane, row, column):
		return (plane * 32) + (row * 4) + column;