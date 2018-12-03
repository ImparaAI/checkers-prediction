import datetime
from checkers.game import Game

class TournamentGame():

	def __init__(self, tournament_id):
		self.tournament_id = tournament_id
		self.moves = []
		self.start_time = None
		self.end_time = None
		self.game = Game()
		self.start()

	def start(self):
		self.start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

	def end(self):
		self.end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

	def move(self, move):
		self.game.move(move)
		self.moves.append(move)
