import numpy as np
from app.model.checkers.action_space import get_action_index
from app.model.checkers.input_builder import build as build_input

class Lesson:

	def __init__(self, node):
		self.input = build_input(node.state)
		self.win_value = None
		self.player_turn = node.state.whose_turn()
		self.action_probabilities = self.build_action_probabilities(node)

	def build_action_probabilities(self, node):
		probabilities = np.zeros(shape = 8 * node.state.board.height * node.state.board.width, dtype = np.float32)

		for child in node.children:
			index = get_action_index(node.state, child.state.moves[-1])
			probabilities[index] = child.visits / node.visits

		return probabilities

	def update_winner(self, winner):
		self.win_value = 0 if winner == None else (1 if winner == player_turn else -1)