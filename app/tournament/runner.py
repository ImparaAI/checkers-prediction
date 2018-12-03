import json
from .storage import storage
from .game.game import TournamentGame
from .game import saver as game_saver
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

		tournament_game = play_game(tournament)

		game_saver.save(tournament_game)

		if tournament_game.game.get_winner() == 1:
			player1_win_count += 1
		elif tournament_game.game.get_winner() == 2:
			player2_win_count += 1
		else:
			draw_count += 1

	print(tournament['id'], player1_win_count, player2_win_count, draw_count)

	storage.complete(tournament['id'], player1_win_count, player2_win_count, draw_count)

def play_game(tournament):
	tournament_game = TournamentGame(tournament['id'])
	player1 = build_player(tournament['player1'])
	player2 = build_player(tournament['player2'])

	while not tournament_game.game.is_over():
		play_turn(tournament_game, player1, player2)

	tournament_game.end()

	return tournament_game

def build_player(config):
	config = json.loads(config)
	classes = {
		'RandomPlayer': RandomPlayer
	}

	return classes[config['name']](config['data'])

def play_turn(tournament_game, player1, player2):
	player = player1 if tournament_game.game.whose_turn() == 1 else player2
	possible_moves = tournament_game.game.get_possible_moves()

	if len(possible_moves) == 1:
		move = possible_moves[0]
	else:
		move = player.get_move(tournament_game.game)

	tournament_game.move(move)
	player1.update_with_new_move(move)
	player2.update_with_new_move(move)