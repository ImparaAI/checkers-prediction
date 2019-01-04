import random

class RandomPlayer():

	def __init__(self, config = {}):
		pass

	def get_move(self, game):
		moves = game.get_possible_moves()
		return random.choice(moves)

	def update_with_new_move(self, move):
		pass

	def build_config(self):
		return {
			'name': 'RandomPlayer',
			'data': {}
		}