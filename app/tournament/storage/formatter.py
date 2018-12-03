def format(tournament):
	return {
		'id': tournament[0],
		'player1': tournament[1],
		'player2': tournament[2],
		'episodeCount': tournament[3],
		'player1WinCount': tournament[4],
		'player2WinCount': tournament[5],
		'draw_count': tournament[6],
		'startTime': tournament[7],
		'endTime': tournament[8],
		'createdAt': tournament[9],
	}