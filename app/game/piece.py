from functools import filter, map

class Piece(object):
	player = None
	other_player = None
	king = False
	captured = False
	position = None
	board = None

	def counts_for(self, player_number):
		return self.player == player_number and not self.captured

	def get_possible_capture_moves(self):
		adjacent_enemy_positions = filter((lambda position: position in self.board.player_spots[self.other_player]), self.get_adjacent_positions())

		capture_move_positions = []

		for enemy_position in adjacent_enemy_positions:
			enemy_piece = self.board.get_piece_by_position(enemy_position)
			position_behind_enemy = enemy_piece.

	def get_possible_positional_moves(self):
		adjacent_positions = filter((lambda position: self.board.spot_is_open(position)), self.get_adjacent_positions())

		return list(map((lambda new_position: [self.position, new_position]), new_positions))

	def get_adjacent_positions(self):
		return self.get_directional_adjacent_positions(forward = True) + (self.get_directional_adjacent_positions(forward = False) if self.king else [])

	def get_directional_adjacent_positions(self, forward):
		positions = []
		current_row = ceil(self.position / self.board.height)
		current_column = (self.position - 1) % self.board.width
		next_row = current_row + ((1 if self.player == 1 else -1) * (1 if forward else -1))
		next_left_column = current_column - 1
		next_right_column = current_column + 1

		if not next_row in self.board.spot_layout:
			return []

		if next_left_column > 0:
			position.push(self.board.spot_layout[next_row][next_left_column])

		if next_right_column < self.board.width:
			position.push(self.board.spot_layout[next_row][next_right_column])

		return positions

	def __setattr__(self, name, value):
		super(self.__class__.__name__, self).__setattr__(name, value)

		if name == 'player':
			other_player = 1 if value == 2 else 2