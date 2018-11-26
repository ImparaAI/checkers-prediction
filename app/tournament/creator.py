import json
from .storage import storage

def create(player1, player2, episodeCount):
	player1_config = json.dumps(player1.build_config())
	player2_config = json.dumps(player2.build_config())

	storage.create(player1_config, player2_config, episodeCount);