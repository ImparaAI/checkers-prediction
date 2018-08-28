from .board import Board

class Game(object):

	def __init__(self):
		self.boards = []
		self.moves = []
		self.move_limit = 500
		self.boards.append(Board())

	def move(self, move):
		if move not in self.get_possible_moves():
			raise ValueError('The provided move is not possible')

		self.boards.append(self.boards[-1].create_new_board_from_move(move))
		self.moves.append(move)

		return self

	def move_limit_reached(self):
		return len(self.boards) > self.move_limit

	def is_over(self):
		return self.move_limit_reached() or not self.get_possible_moves();

	def get_winner(self):
		if not self.boards[-1].count_movable_player_pieces(1):
			return 2
		elif not self.boards[-1].count_movable_player_pieces(2):
			return 1
		else:
			return None

	def get_possible_moves(self):
		return self.boards[-1].get_possible_moves()

	def whose_turn(self):
		return self.boards[-1].player_turn