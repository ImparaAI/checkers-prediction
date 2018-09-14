from model.model import Model
from checkers.game import Game
from model import input_builder

def predict(moves):
	game = build_game(moves)
	montecarlo = MonteCarlo(Node(game))
	montecarlo.child_finder = child_finder

	montecarlo.simulate(50)

	chosen_node = montecarlo.make_choice()

	#montecarlo go and do you shit with these params


	return builder.build().predict(request)

def child_finder(node):
	prediction = self.model.predict(self.build_input(node.state))
	node.update_win_value(prediction.win_value)

	prediction.action_probabilities = [.91, .02, .00003, ...]

	for move in node.state.get_possible_moves():

		prediction.action_probabilities


		child = Node(deepcopy(node.state))
		child.state.move(move)
		child.policy_value = self.get_policy_value(move, node.state.whose_turn())
		node.add_child(child)


def build_game(moves):
	game = Game()

	for move in moves:
		game.move(move)

	return game