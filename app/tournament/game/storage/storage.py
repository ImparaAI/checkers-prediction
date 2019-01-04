from . import formatter
from app.database import database

def create(tournament_id, moves, start_time, end_time):
	inputs = (tournament_id, moves, start_time, end_time)

	return database.insert("INSERT INTO tournament_games (tournamentId, moves, startTime, endTime) VALUES (?, ?, ?, ?)", inputs)

def get(id):
	game = database.fetchone("SELECT * FROM tournament_games WHERE id = ?", (id,))

	return formatter.format(game)