import unittest
from random import randint
from app.montecarlo.node import Node
from app.montecarlo.montecarlo import MonteCarlo

class test_montecarlo(unittest.TestCase):

	def test_possible_moves(self):
		montecarlo = MonteCarlo(Node(10000))
		montecarlo.child_finder = self.child_finder

		for i in range(50):
			montecarlo.roll_out()

		montecarlo.get_most_searched_child()
		montecarlo.get_highest_value_child()

		self.assertEqual(True, True);

	def child_finder(self, node):
		children = []

		for i in range(5):
			child_node = Node(node.state / randint(2, 9))

			if child_node.state < 1 and child_node.state > 0.5:
				child_node.update_win_value(1)
			elif child_node.state < 0.5 and child_node.state > 0:
				child_node.update_win_value(-1)

			children.push(child_node)

		return children