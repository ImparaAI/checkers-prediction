class MonteCarlo:

	def __init__(self, root_node):
		self.root_node = root_node
		self.child_finder = None

	def change_root_node(self, root_node):
		self.root_node = root_node
		#do some tree pruning

	def simulate(self):
		current_node = self.root_node

		while current_node.expanded:
			current_node = current_node.get_preferred_child()

		self.expand(current_node)

	def expand(self, node):
		for child_node in self.child_finder(node):
			node.children.push(child_node)

			if not child_node.visits

	def roll_out(self, node):

		unvisited_node =
		if not node.children:
			node.children = self.child_finder(node)

			for child_node in node.children:
				child_node