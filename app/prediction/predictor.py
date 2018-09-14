import numpy as np
from copy import deepcopy
from app.game.game import Game
from app.model.model import Model
from app.model import action_space
from app.model import input_builder
from app.montecarlo.node import Node
from app.montecarlo.montecarlo import MonteCarlo

def predict(moves):
	game = build_game(moves)
	montecarlo = MonteCarlo(Node(game))
	montecarlo.child_finder = child_finder

	montecarlo.simulate(5)

	chosen_node = montecarlo.make_choice()

	return chosen_node.state.moves[-1]

def child_finder(node):
	model = Model((34, 8, 4), 8 * 8 * 4)
	prediction = model.predict( np.array([input_builder.build(node.state)]))
	node.update_win_value(prediction['win_value'])

	for move in node.state.get_possible_moves():
		child = build_child(node, move, prediction['action_probabilities'])
		node.add_child(child)

def build_child(parent, move, action_probabilities):
		child = Node(deepcopy(parent.state))
		child.state.move(move)

		action_index = action_space.get_action_index(parent.state, move)
		child.policy_value = action_probabilities[action_index]

		return child

def build_game(moves):
	game = Game()

	for move in moves:
		game.move(move)

	return game