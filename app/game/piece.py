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


	def get_forward_diagonal_posiitons(self):
