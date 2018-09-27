import random
from .lesson import Lesson
from app.player import Player
from checkers.game import Game
from app.model.checkers import model as checkers_model

def train(model_name):
	Trainer(model_name).train()

class Trainer:

	def __init__(self, model_name):
		self.model = checkers_model.build(model_name)
		self.game = None
		self.lessons = []
		self.batches = 20
		self.batch_size = 200

	def train(self):
		for i in range(3):
			print('game ' + str(i) + ' starting')
			self.play_game()
			print('game ' + str(i) + ' over')

		self.update_model()

	def play_game(self):
		self.game = Game()
		self.player1 = Player(1, self.game, self.model)
		self.player2 = Player(2, self.game, self.model)

		while not self.game.is_over():
			self.play_turn()

		self.set_lesson_winners()

	def play_turn(self):
		player = self.player1 if self.game.whose_turn() == 1 else self.player2
		move = player.simulate().get_next_move()

		self.lessons.append(Lesson(player.montecarlo.root_node))

		self.move(move)
		print('moved', move)

	def move(self, move):
		self.player1.move(move)
		self.player2.move(move)
		self.game.move(move)

	def set_lesson_winners(self):
		winner = self.game.get_winner()

		for lesson in self.lessons:
			lesson.update_winner(winner)

	def update_model(self):
		for i in range(self.batches):
			batch_lessons = random.sample(self.lessons, min(self.batch_size, len(self.lessons)))
			inputs, win_values, action_probabilities = ([], [], [])

			for lesson in batch_lessons:
				inputs.append(lesson.input)
				win_values.append(lesson.win_value)
				action_probabilities.append(lesson.action_probabilities)

			self.model.train(inputs, win_values, action_probabilities)

		self.model.save()