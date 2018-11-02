import random
from .lesson import Lesson
from app.player import Player
from checkers.game import Game
from app.model.checkers import model as checkers_model

def train(model_name, episodes = 5):
	Trainer(model_name).train(episodes)

class Trainer:

	def __init__(self, model_name):
		self.model = checkers_model.build(model_name)
		self.game = None
		self.game_boards = []
		self.lessons = []
		self.max_batch_size = 1024
		self.preferred_batch_count = 20

	def train(self, episodes):
		for i in range(episodes):
			self.play_game()
			print('game ' + str(i) + ' over')

		self.update_model()

	def play_game(self):
		self.game = Game()
		self.game_boards = []
		self.player1 = Player(1, self.game, self.model)
		self.player2 = Player(2, self.game, self.model)

		while not self.game.is_over():
			self.play_turn()

		self.set_lesson_winners()

	def play_turn(self):
		player = self.player1 if self.game.whose_turn() == 1 else self.player2
		move = player.simulate().get_next_move()

		self.game_boards.append(player.montecarlo.root_node.state.board)
		self.lessons.append(Lesson(player.montecarlo.root_node, self.game_boards[-8:]))

		self.move(move)

	def move(self, move):
		self.player1.move(move)
		self.player2.move(move)
		self.game.move(move)

	def set_lesson_winners(self):
		winner = self.game.get_winner()

		for lesson in self.lessons:
			lesson.update_winner(winner)

	def update_model(self):
		batch_size = min(self.max_batch_size, len(self.lessons) // self.preferred_batch_count)
		random.shuffle(self.lessons)
		print('batch_size: ' + str(batch_size) )

		while len(self.lessons):
			inputs, win_values, action_probabilities = self.build_training_values(batch_size)
			self.model.train(inputs, win_values, action_probabilities)

		self.model.save()

	def build_training_values(self, batch_size):
		inputs, win_values, action_probabilities = ([], [], [])

		for x in range(1, batch_size):
			if len(self.lessons):
				lesson = self.lessons.pop()
				inputs.append(lesson.input)
				win_values.append(lesson.win_value)
				action_probabilities.append(lesson.action_probabilities)

		return inputs, win_values, action_probabilities