from .board import Board

class Game:

	boards = []
	move_limit = 500

	def __init__(self):
		self.boards.append(Board())

	def set_move_limit(self, move_limit):
		self.move_limit = move_limit

	def move(self, starting_position, ending_position):
		pass

	def move_limit_reached(self):
		return len(self.boards) > self.move_limit

	def is_over(self):
		return self.move_limit_reached() or not self.get_possible_moves();

	def get_winner(self):
		if not self.boards[-1].count_player_pieces(1):
			return 2
		elif not self.boards[-1].count_player_pieces(2):
			return 1
		else:
			return 0

	def get_possible_moves(self):
		pass