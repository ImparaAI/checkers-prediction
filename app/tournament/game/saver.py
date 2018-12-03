import json
from .storage import storage

def save(game):
	moves = json.dumps(game.moves)
	storage.create(game.tournament_id, moves, game.start_time, game.end_time)