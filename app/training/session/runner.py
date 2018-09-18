from copy import deepcopy
from checkers.game import Game
from montecarlo.node import Node
from app.model.model import Model
from montecarlo.montecarlo import MonteCarlo

class Runner:

	def __init__(self):
		self.model = Model()
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