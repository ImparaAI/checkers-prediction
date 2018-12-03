def format(game):
	return {
		'id': game[0],
		'tournamentId': game[1],
		'moves': game[2],
		'startTime': game[3],
		'endTime': game[4],
		'createdAt': game[5],
	}