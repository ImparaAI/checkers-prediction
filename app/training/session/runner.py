from copy import deepcopy
from app.model import builder
from checkers.game import Game
from montecarlo.node import Node
from montecarlo.montecarlo import MonteCarlo

class Runner:

	def __init__(self):
		self.model = builder.build()
		self.game = None
		self.montecarlo = None

	def run(self):
		for i in range(1000):
			self.play_game()

		self.train()

	def play_game(self):
		self.game = Game()
		self.montecarlo = MonteCarlo(Node(self.game))
		self.montecarlo.child_finder = self.child_finder

		while not self.game.is_over():
			self.play_turn()

		self.store_game_training_data()

	def play_turn(self):
		for i in range(50):
			montecarlo.simulate()

		chosen_node = montecarlo.make_choice()
		self.montecarlo.change_root_node(chosen_node)
		self.game.move(chosen_node.state.moves[-1])

	def child_finder(self, node):
		prediction = self.model.predict(self.build_input(node.state))
		node.update_win_value(prediction.win_value)

		for move in node.state.get_possible_moves():
			child = Node(deepcopy(node.state))
			child.state.move(move)
			child.policy_value = self.get_policy_value(child.state, prediction.policy_values)
			node.add_child(child)

	def build_input(self, game):
		pass

	def get_policy_value(self, game, policy_values):
		pass