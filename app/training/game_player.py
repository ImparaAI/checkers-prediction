from .lesson import Lesson
from app.player import Player
from checkers.game import Game

from datetime import datetime

game = None
player1 = None
player2 = None
lessons = []
game_boards = []

def play_game(lesson_queue, prediction_request_queue, prediction_result_queue):
	startTime = datetime.now()
	global game, player1, player2

	class Model:
		def predict(self, input):
			prediction_request_queue.put(input)
			prediction_request_queue.join()

			prediction = prediction_result_queue.get()
			prediction_result_queue.task_done()

			return prediction

	game = Game()
	player1 = Player(1, game, Model())
	player2 = Player(2, game, Model())

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