import json
from .storage import storage
from checkers.game import Game
from .players.random_player import RandomPlayer

def run_by_id(id):
	tournament = storage.get(id)

	run(tournament)

def run_next():
	tournament = storage.get_next()

	run(tournament)

def run(tournament):
	player1_win_count = 0
	player2_win_count = 0
	draw_count = 0

	storage.start(tournament['id'])

	for gameNumber in range(tournament['episodeCount']):

		game = play_game(tournament)

		#save the game results (move list, probabilities of each move)

		if game.get_winner() == 1:
			player1_win_count += 1
		elif game.get_winner() == 2:
			player2_win_count += 1
		else:
			draw_count += 1

	print(tournament['id'], player1_win_count, player2_win_count, draw_count)
	storage.complete(tournament['id'], player1_win_count, player2_win_count, draw_count)

def play_game(tournament):
	game = Game()
	player1 = build_player(tournament['player1'])
	player2 = build_player(tournament['player2'])

	while not game.is_over():
		play_turn(game, player1, player2)

	return game

def build_player(config):
	config = json.loads(config)
	classes = {
		'RandomPlayer': RandomPlayer
	}

	return classes[config['name']](config['data'])

def play_turn(game, player1, player2):
	player = player1 if game.whose_turn() == 1 else player2
	possible_moves = game.get_possible_moves()

	if len(possible_moves) == 1:
		move = possible_moves[0]
	else:
		move = player.get_move(game)

	game.move(move)
	player1.update_with_new_move(move)
	player2.update_with_new_move(move)