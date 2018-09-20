import numpy as np
from copy import deepcopy
from montecarlo.node import Node
from app.model.model import Model
from app.model.checkers import action_space
from app.model.checkers import input_builder
from montecarlo.montecarlo import MonteCarlo

import random

class Player:

	def __init__(self, number, game, model):
		self.number = number
		self.game = game
		self.model = model
		self.montecarlo = MonteCarlo(Node(game))
		self.montecarlo.child_finder = self.montecarlo_child_finder

	def simulate(self, simulation_count = 5):
		self.check_turn()

		try:
			self.montecarlo.simulate(simulation_count)
		except IndexError:
			print(self.game.get_possible_moves())
			raise ValueError('ok things are bad')

		return self

	def get_next_move(self):
		self.check_turn()

		chosen_node = self.montecarlo.make_choice()

		return chosen_node.state.moves[-1]

	def move(self, move):
		found = False

		for child in self.montecarlo.root_node.children:
			if move == child.state.moves[-1]:
				self.montecarlo.root_node = child
				found = True
				break

		if not found:
			print('couldnt find child matching move', move, self.montecarlo.root_node.children)

	def check_turn(self):
		if self.number != self.game.whose_turn():
			raise ValueError("It isn't this player's turn")

	def montecarlo_child_finder(self, node, montecarlo):
		prediction = self.model.predict(np.array([input_builder.build(node.state)]))
		is_current_player = node.state.whose_turn() == montecarlo.root_node.state.whose_turn()

		node.update_win_value(prediction['win_value'] * (1 if is_current_player else -1))

		for move in node.state.get_possible_moves():
			child = self.build_child(node, move, prediction['action_probabilities'])
			node.add_child(child)

	def build_child(self, parent, move, action_probabilities):
		child = Node(deepcopy(parent.state))
		child.state.move(move)
		child.move = move

		action_index = action_space.get_action_index(parent.state, move)
		child.policy_value = action_probabilities[action_index]

		return child