from copy import deepcopy
from app.game.game import Game
from app.montecarlo.node import Node
from app.montecarlo.montecarlo import MonteCarlo

def run():


def play_game():
	montecarlo = MonteCarlo(Node(Game()))
	montecarlo.child_finder = child_finder

	for i in range(50):
		montecarlo.simulate()

	chosen_node = montecarlo.make_choice()
	self.assertIs(chosen_node.state, 1)

def child_finder(node):
	for move in node.state.get_possible_moves():
		child = Node(deepcopy(node.state))
		child.state.move(move)
		node.add_child(child)