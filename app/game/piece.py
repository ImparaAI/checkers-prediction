from math import ceil

class Piece(object):

	def __init__(self):
		self.player = None
		self.other_player = None
		self.king = False
		self.captured = False
		self.position = None
		self.board = None

	def counts_for(self, player_number):
		return self.player == player_number and not self.captured

	def get_possible_capture_moves(self):
		adjacent_enemy_positions = filter((lambda position: position in self.board.searcher.get_pieces_by_player(self.other_player)), self.get_adjacent_positions())
		capture_move_positions = []
		current_row = self.get_row()
		current_column = self.get_column()

		for enemy_position in adjacent_enemy_positions:
			enemy_piece = self.board.get_piece_by_position(enemy_position)
			position_behind_enemy = self.get_position_behind_enemy(enemy_piece)

			if (position_behind_enemy != None) and self.board.position_is_open(position_behind_enemy):
				capture_move_positions.append(position_behind_enemy)

		return self.create_moves_from_new_positions(capture_move_positions)

	def get_position_behind_enemy(self, enemy_piece):
		enemy_column = enemy_piece.get_column()
		enemy_row = enemy_piece.get_row()
		column_adjustment = -1 if current_row % 2 == 0 else 1
		column_behind_enemy = current_column + column_adjustment if current_column == enemy_column else enemy_column
		row_behind_enemy = enemy_row + (enemy_row - current_row)

		return self.board.position_layout.get(row_behind_enemy, {}).get(column_behind_enemy)

	def get_possible_positional_moves(self):
		new_positions = list(filter((lambda position: self.board.position_is_open(position)), self.get_adjacent_positions()))

		return self.create_moves_from_new_positions(new_positions)

	def create_moves_from_new_positions(self, new_positions):
		return [[self.position, new_position] for new_position in new_positions]

	def get_adjacent_positions(self):
		return self.get_directional_adjacent_positions(forward = True) + (self.get_directional_adjacent_positions(forward = False) if self.king else [])

	def get_column(self):
		return (self.position - 1) % self.board.width

	def get_row(self):
		return ceil(self.position / self.board.width) - 1

	def get_directional_adjacent_positions(self, forward):
		positions = []
		current_row = self.get_row()
		next_row = current_row + ((1 if self.player == 1 else -1) * (1 if forward else -1))

		if not next_row in self.board.position_layout:
			return []

		next_column_indexes = self.get_next_column_indexes(current_row, self.get_column())

		return [self.board.position_layout[next_row][column_index] for column_index in next_column_indexes]

	def get_next_column_indexes(self, current_row, current_column):
		column_indexes = [current_column, current_column + 1] if current_row % 2 == 0 else [current_column - 1, current_column]

		return filter((lambda column_index: column_index >= 0 and column_index < self.board.width), column_indexes)

	def __setattr__(self, name, value):
		super(Piece, self).__setattr__(name, value)

		if name == 'player':
			self.other_player = 1 if value == 2 else 2