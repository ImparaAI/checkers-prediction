from copy import deepcopy
from functools import reduce
from .board_searcher import BoardSearcher
from .board_initializer import BoardInitializer

class Board(object):

	player_turn = 1
	width = 4
	height = 8
	position_count = width * height
	rows_per_user_with_pieces = 3
	position_layout = {}
	pieces = []
	piece_requiring_further_capture_moves = None
	searcher = BoardSearcher()

	def __init__(self):
		BoardInitializer(self).initialize()

	def count_player_pieces(player_number = 1):
		return reduce((lambda count, piece: count + (1 if piece.counts_for(player_number) else 0)), self.pieces)

	def get_possible_moves(self):
		capture_moves = self.get_possible_capture_moves()

		return capture_moves if capture_moves else self.get_possible_positional_moves()

	def get_possible_capture_moves(self):
		return reduce((lambda moves, piece: moves + piece.get_possible_capture_moves()), self.searcher.get_pieces_in_play(), [])

	def get_possible_positional_moves(self):
		return reduce((lambda moves, piece: moves + piece.get_possible_positional_moves()), self.searcher.get_pieces_in_play(), [])

	def position_is_open(self, position):
		return not self.searcher.get_piece_by_position(position)

	def create_new_board_from_move(self, move):
		new_board = deepcopy(self)

		if move in self.get_possible_capture_moves():
			new_board.perform_capture_move(move)
		else:
			new_board.perform_positional_move(move)

		return new_board

	def perform_capture_move(self, move):
		self.move_piece(move)
		further_capture_moves_for_piece = [capture_move for capture_move in self.get_possible_capture_moves() if move[1] == capture_move[0]]

		if further_capture_moves_for_piece:
			self.piece_requiring_further_capture_moves = self.searcher.get_piece_by_position(move[1])
		else:
			self.piece_requiring_further_capture_moves = None
			self.switch_turn()

	def perform_positional_move(self, move):
		self.move_piece(move)
		self.switch_turn()

	def switch_turn(self):
		self.player_turn = 1 if self.player_turn == 2 else 2

	def move_piece(self, move):
		self.searcher.get_piece_by_position(move[0]).position = move[1]
		self.searcher.build(self)

	def get_position_from_column_and_row(self, column, row):
		return self.position_layout.get(row, {}).get(column, None)

	def __setattr__(self, name, value):
		super(Board, self).__setattr__(name, value)

		if name == 'pieces':
			self.searcher.build(self)