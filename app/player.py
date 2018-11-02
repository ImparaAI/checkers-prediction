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
		self.montecarlo = self.build_montecarlo()

	def build_montecarlo(self):
		root_node = Node(self.game)
		root_node.player_number = self.game.whose_turn()

		montecarlo = MonteCarlo(root_node)
		montecarlo.child_finder = self.montecarlo_child_finder

		return montecarlo

	def simulate(self, simulation_count = 5):
		self.montecarlo.simulate(simulation_count)

		return self

	def get_next_move(self):
		chosen_node = self.montecarlo.make_choice()

		return chosen_node.state.moves[-1]

	def move(self, move):
		if not self.montecarlo.root_node.expanded:
			self.add_child_to_parent(self.montecarlo.root_node, move)

		for child in self.montecarlo.root_node.children:
			if move == child.state.moves[-1]:
				self.montecarlo.root_node = child
				break

	def montecarlo_child_finder(self, node, montecarlo):
		if node.state.is_over():
			win_value = self.get_end_game_win_value(node.state, montecarlo)
			node.update_win_value(win_value)
			return

		prediction = self.model.predict(np.array([input_builder.build(node.state)]))
		is_current_player = node.state.whose_turn() == montecarlo.root_node.state.whose_turn()

		node.update_win_value(prediction['win_value'] * (1 if is_current_player else -1))

		for move in node.state.get_possible_moves():
			child = self.add_child_to_parent(node, move)
			action_index = action_space.get_action_index(node.state, move)
			child.policy_value = prediction['action_probabilities'][action_index]

	def add_child_to_parent(self, parent, move):
		child = Node(deepcopy(parent.state))
		child.state.move(move)
		child.state.boards = []
		child.player_number = child.state.whose_turn()

		parent.add_child(child)

		return child

	def get_end_game_win_value(self, state, montecarlo):
		winner = state.get_winner()

		if winner == None:
			return 0

		return 1 if winner == montecarlo.root_node.state.whose_turn() else -1
