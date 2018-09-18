import numpy as np
from copy import deepcopy
from checkers.game import Game
from montecarlo.node import Node
from app.model.model import Model
from app.model.checkers import action_space
from app.model.checkers import input_builder
from montecarlo.montecarlo import MonteCarlo

def predict(moves, simulation_count = 5):
	game = build_game(moves)
	montecarlo = MonteCarlo(Node(game))
	montecarlo.child_finder = child_finder

	montecarlo.simulate(simulation_count)

	chosen_node = montecarlo.make_choice()

	return chosen_node.state.moves[-1]

def child_finder(node, montecarlo):
	model = Model((34, 8, 4), 8 * 8 * 4)
	prediction = model.predict(np.array([input_builder.build(node.state)]))
	is_current_player = node.state.whose_turn() == montecarlo.root_node.state.whose_turn()

	node.update_win_value(prediction['win_value'] * (1 if is_current_player else -1))

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