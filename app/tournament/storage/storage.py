import datetime
from . import formatter
from app.database import database

date_format = '%Y-%m-%d %H:%M:%S'

def create(player1, player2, episodeCount):
	inputs = (player1, player2, episodeCount)

	database.execute("DELETE FROM tournaments where 1")
	return database.insert("INSERT INTO tournaments (player1, player2, episodeCount) VALUES (?, ?, ?)", inputs)

def start(id):
	time = datetime.datetime.now().strftime(date_format)

	database.execute("UPDATE tournaments SET startTime = ? WHERE id = ?", (time, id))

def complete(id, player1_win_count, player2_win_count, draw_count):
	time = datetime.datetime.now().strftime(date_format)
	inputs = (time, player1_win_count, player2_win_count, draw_count, id)

	database.execute("UPDATE tournaments SET endTime = ?, player1_win_count = ?, player2_win_count = ?, draw_count = ? WHERE id = ?", inputs)

def get(id):
	tournament = database.fetchone("SELECT * FROM tournaments WHERE id = ?", id)

	return formatter.format(tournament)

def get_next():
	tournament = database.fetchone("SELECT * FROM tournaments WHERE startTime IS NULL ORDER BY id ASC")

	if tournament:
		return formatter.format(tournament)