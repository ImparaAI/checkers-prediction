from .lesson import Lesson
from app.player import Player
from checkers.game import Game

from datetime import datetime

game = None
player1 = None
player2 = None
lessons = []
game_boards = []

class MultiprocessModel:
	def __init__(self, prediction_request):
		self.prediction_request = prediction_request

	def predict(self, input):
		self.prediction_request.set_input(input)

		while not self.prediction_request.get_response():
			continue

		return self.prediction_request.get_response()

def play_games(episode_count, lesson_queue, prediction_request):
	for i in range(episode_count):
		play_game(lesson_queue, prediction_request)

def play_game(lesson_queue, prediction_request):
	startTime = datetime.now()
	global game, player1, player2

	game = Game()
	player1 = Player(1, game, MultiprocessModel(prediction_request))
	player2 = Player(2, game, MultiprocessModel(prediction_request))

	while not game.is_over():
		play_turn()

	finalize_lessons(lesson_queue)

	print('game over', datetime.now() - startTime)

def play_turn():
	player = player1 if game.whose_turn() == 1 else player2
	move = player.simulate().get_next_move()

	game_boards.append(player.montecarlo.root_node.state.board)
	lessons.append(Lesson(player.montecarlo.root_node, game_boards[-8:]))

	make_move(move)

def make_move(move):
	player1.move(move)
	player2.move(move)
	game.move(move)

def finalize_lessons(lesson_queue):
	winner = game.get_winner()

	for lesson in lessons:
		lesson.update_winner(winner)
		lesson_queue.put(lesson)