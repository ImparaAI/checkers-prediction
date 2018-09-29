import datetime
from . import formatter
from database import database

date_format = '%Y-%m-%d %H:%M:%S'

def stop_active_sessions():
	database.execute("UPDATE training_sessions SET deactivated = 1 WHERE deactivated = 0 AND endTime IS NULL AND startTime IS NOT NULL")

def get_active_session():
	session = database.fetchone("SELECT * FROM training_sessions WHERE deactivated = 0 AND endTime IS NULL AND startTime IS NOT NULL LIMIT 1")

	if session:
		return formatter.format(session)

def create_new_session(session):
	inputs = (session['name'], session['episodeLimit'], session['secondsLimit'])
	database.execute("INSERT INTO training_sessions (name, episodeLimit, secondsLimit) VALUES (%s, %s, %s)", inputs)

	return int(database.fetchone("SELECT LAST_INSERT_ID()")[0])

def get_next_session():
	active_session = get_active_session()

	if active_session:
		return

	session = database.fetchone("SELECT * FROM training_sessions WHERE deactivated = 0 AND endTime IS NULL AND startTime IS NULL LIMIT 1")

	if session:
		return formatter.format(session)

def activate(id):
	time = datetime.datetime.now().strftime(date_format)

	database.execute("UPDATE training_sessions SET startTime = %s WHERE id = %s", (time, id))

def boost_episode_count(id, episodes):
	database.execute("UPDATE training_sessions SET episodeCount = episodeCount + %s WHERE id = %s", (episodes, id))

def is_active(id):
	return not not database.fetchone("SELECT id FROM training_sessions WHERE deactivated = 0 AND endTime IS NULL AND startTime IS NOT NULL")

def finish(id):
	time = datetime.datetime.now().strftime(date_format)

	database.execute("UPDATE training_sessions SET endTime = %s WHERE id = %s", (time, id))

def get_latest_session():
	session = database.fetchone("SELECT * FROM training_sessions WHERE startTime IS NOT NULL ORDER BY startTime")

	if session:
		return formatter.format(session)

def get_all():
	result = database.fetchall("SELECT * FROM training_sessions")

	return formatter.format_many(result)