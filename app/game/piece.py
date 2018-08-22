class Piece:
	player = None
	king = False
	captured = False
	position = None

	def __init__(self, player):
		self.player = player

	def counts_for(self, player_number):
		return self.player == player_number and not self.captured