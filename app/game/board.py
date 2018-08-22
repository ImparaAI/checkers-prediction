from math import ceil
from .piece import Piece
from functools import reduce

class Board(object):

	player_turn = 1
	pieces = []
	open_spots = []
	filled_spots = []
	width = 4
	height = 8
	spot_count = width * height
	rows_per_user_with_pieces = 3
	spot_layout = {}

	def __init__(self):
		set_layout()
		set_starting_pieces()

	def set_layout(self):
		self.spot_layout = {}
		spot = 1

		for row in range(self.height):
			self.spot_layout[row] = {}

			for column in range(self.width):
				self.spot_layout[row][column] = spot
				spot += 1

	def set_starting_pieces(self):
		pieces = []
		starting_piece_count = self.width * self.rows_per_user_with_pieces
		first_player_starting_spots = range(1, starting_piece_count + 1)
		second_player_starting_spots = range(self.spot_count - starting_piece_count + 1, self.spot_count + 1)

		for row in self.spot_layout:
			for spot in row:
				if spot in first_player_starting_spots:
					player = 1
				elif spot in second_player_starting_spots:
					player = 2
				else:
					continue

				piece = Piece()
				piece.player = player
				piece.position = spot
				piece.board = self
				pieces.push(piece)

		self.pieces = pieces

	def count_player_pieces(player_number = 1):
		return reduce((lambda count, piece: count + (1 if piece.counts_for(player_number) else 0)), self.pieces)

	def get_possible_moves(self):
		capture_moves = self.get_possible_capture_moves()

		return capture_moves if capture_moves else self.get_possible_positional_moves()

	def get_possible_capture_moves(self):
		return reduce((lambda moves, piece: moves + piece.get_possible_capture_moves()), self.pieces)

	def get_possible_positional_moves(self):
		return reduce((lambda moves, piece: moves + piece.get_possible_positional_moves()), self.pieces)

	def spot_is_open(self, spot):
		return spot in self.open_spots

	def get_forward_diagonal_posiitons(self, piece):
		current_row = ceil()

	def create_new_board_from_move(self, move):
		pass

	def update_piece_data(self):
		self.update_filled_spots()
		self.update_open_spots()

	def update_filled_spots(self):
		self.filled_spots = reduce((lambda open_spots, piece: open_spots + [piece.position]), self.pieces)

	def update_open_spots(self):
		self.open_spots = [spot for spot in range(1, self.spot_count) if not spot in self.filled_spots]

	def __setattr__(self, name, value):
		super(Board, self).__setattr__(name, value)

		if name == 'pieces':
			self.update_piece_data()