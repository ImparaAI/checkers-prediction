from random import choice

class MonteCarlo:

	def __init__(self, root_node):
		self.root_node = root_node
		self.child_finder = None
		self.node_evaluator = lambda child: None

	def change_root_node(self, root_node):
		self.root_node = root_node
		#do some tree pruning

	def make_choice(self):


	def simulate(self):
		current_node = self.root_node

		while current_node.expanded:
			current_node = current_node.get_preferred_child()

		self.expand(current_node)

	def expand(self, node):
		node.children = self.child_finder(node)

		for child in node.children:
			child_win_value = self.node_evaluator(child)

			if child_win_value != None:
				child.update_win_value(child_win_value)

			if not child.is_scorable():
				self.random_rollout(child)
				child.children = []

	def random_rollout(self, node):
		self.child_finder(node)
		child = choice(node.children)
		node.children = [child]
		child_win_value = self.node_evaluator(child)

		if child_win_value != None:
			node.update_win_value(child_win_value)
		else:
			self.random_rollout(child)