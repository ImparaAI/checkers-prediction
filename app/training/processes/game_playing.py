from app.player import Player
from checkers.game import Game
from app.training.lesson import Lesson

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

def play_games(episode_count, prediction_request, lesson_pipe, lesson_signal, simulation_depth):
	print('game playing process started')

	for i in range(episode_count):
		play_game(prediction_request, simulation_depth)

	lesson_signal.value = 1
	lesson_pipe.send(lessons)
	lesson_pipe.close()

def play_game(prediction_request, simulation_depth):
	startTime = datetime.now()
	global game, player1, player2

	game = Game()
	player1 = Player(1, game, MultiprocessModel(prediction_request))
	player2 = Player(2, game, MultiprocessModel(prediction_request))

	while not game.is_over():
		play_turn(simulation_depth)

	finalize_lessons()

	print('game over', datetime.now() - startTime)

def play_turn(simulation_depth):
	player = player1 if game.whose_turn() == 1 else player2
	possible_moves = game.get_possible_moves()

	if len(possible_moves) == 1:
		move = possible_moves[0]
	else:
		move = player.simulate(simulation_depth).get_next_move()

	lessons.append(Lesson(player.montecarlo.root_node, player.game_boards[-8:]))

	make_move(move)

def make_move(move):
	game.move(move)
	player1.update_with_new_move(move)
	player2.update_with_new_move(move)

def finalize_lessons():
	winner = game.get_winner()

	for lesson in lessons:
		lesson.update_winner(winner)