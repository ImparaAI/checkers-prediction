import inspect
from .piece import Piece
from functools import reduce

class Board:

	player_turn = 1
	pieces = []

	def __init__(self):
		set_starting_pieces()

	def set_starting_pieces(self):
		for i in range(1, 13):
			piece = Piece()
			piece.player = 1
			piece.position = i
			piece.board = self
			self.pieces.push(piece)

		for i in range(13, 33):
			piece = Piece()
			piece.player = 2
			piece.position = i
			piece.board = self
			self.pieces.push(piece)

	def count_player_pieces(player_number = 1):
		return reduce((lambda count, piece: count + (1 if piece.counts_for(player_number) else 0)), self.pieces)

	def get_possible_moves(self):
		capture_moves = self.get_possible_capture_moves()

		return capture_moves if capture_moves else self.get_possible_positional_moves()

	def get_possible_capture_moves(self):
		return reduce((lambda moves, piece: moves + piece.get_possible_capture_moves()), self.pieces)

	def get_possible_positional_moves(self):
		return reduce((lambda moves, piece: moves + piece.get_possible_positional_moves()), self.pieces)

	def create_new_board_from_move(self, move):
		pass