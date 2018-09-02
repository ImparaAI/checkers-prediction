class Node:

	def __init__(self, state):
		self.state = state
		self.win_value = None
		self.visits = 0
		self.children = []

	def update_win_value(self, value):
		self.win_value += value
		self.visits += 1