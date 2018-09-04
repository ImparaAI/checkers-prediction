import unittest
from random import randint
from functools import reduce
from app.montecarlo.node import Node
from app.montecarlo.montecarlo import MonteCarlo

class test_montecarlo(unittest.TestCase):

	def test_choice_is_valued(self):
		montecarlo = MonteCarlo(Node(1000))
		montecarlo.child_finder = self.child_finder
		montecarlo.node_evaluator = self.node_evaluator

		for i in range(50):
			montecarlo.roll_out()

		max_visits = reduce((lambda max_visits, child: max_visits if max_visits >= child.visits else child.visits), montecarlo.children, 0)
		chosen_node = montecarlo.make_choice()

		self.assertEqual(chosen_node.visits, max_visits);

	def child_finder(self, node):
		for i in range(5):
			child_node = Node(node.state / randint(2, 9))
			child_node.set_policy_value(ai.child.policy)
			node.add_child(child_node)

		node.update_win_value(ai.w)

	def node_evaluator(self, node):
		if child_node.state < 1 and child_node.state > 0.5:
			return 1
		elif child_node.state < 0.5 and child_node.state > 0:
			return -1