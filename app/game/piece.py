from functools import map

class Piece(object):
	player = None
	king = False
	captured = False
	position = None
	board = None

	def counts_for(self, player_number):
		return self.player == player_number and not self.captured

	def get_possible_capture_moves(self):
		pass

	def get_possible_positional_moves(self):
		new_positions = self.get_forward_adjacent_diagonal_positions()

		if self.king:
			new_positions += self.get_backward_adjacent_diagonal_positions()

		return list(map((lambda new_position: [self.position, new_position]), new_positions))

	def get_forward_adjacent_diagonal_positions(self):
		return self.get_adjacent_diagonal_positions()

	def get_backward_adjacent_diagonal_positions(self):
		return self.get_adjacent_diagonal_positions(False)

	def get_adjacent_diagonal_positions(self, forward = True):
		positions = []
		current_row = ceil(self.position / self.board.height)
		current_column = (self.position - 1) % self.board.width
		next_row = current_row + ((1 if self.player == 1 else -1) * (1 if forward else -1))

		if not next_row in self.board.spot_layout:
			return []

		left_position = current_column - 1 if current_column - 1 > 0 else None
		right_position = current_column + 1 if current_column + 1 > 0 else None

		if self.board.spot_is_open(left_position):
			positions.push(left_position)

		if self.board.spot_is_open(right_position):
			positions.push(right_position)