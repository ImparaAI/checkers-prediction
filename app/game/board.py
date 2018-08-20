import inspect
from .piece import Piece

class Board:

	player_turn = 1
	rows = [
		[Piece(1), Piece(1), Piece(1), Piece(1)],
		[Piece(1), Piece(1), Piece(1), Piece(1)],
		[Piece(1), Piece(1), Piece(1), Piece(1)],
		[None, None, None, None],
		[None, None, None, None],
		[Piece(2), Piece(2), Piece(2), Piece(2)],
		[Piece(2), Piece(2), Piece(2), Piece(2)],
		[Piece(2), Piece(2), Piece(2), Piece(2)]
	]

	def set(self, state = None):
		if state:
			pass

	def count_player_pieces(player_number = 1):
		count = 0

		for row in self.rows:
			for spot in row:
				if isinstance(spot, Piece) and spot.player == player_number:
					count += 1

		return count

	def get_possible_moves(self):
		pass

	def create_new_board_from_move(self, move):
		pass