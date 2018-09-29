import datetime

def format_many(sessions):
	pass

def format(session):
	date_format = '%Y-%m-%d %H:%M:%S'

	return {
		'id': session[0],
		'name': session[1],
		'episodeCount': session[2],
		'episodeLimit': session[3],
		'secondsLimit': session[4],
		'deactivated': bool(session[5]),
		'startTime': session[6],
		'endTime': session[7],
		'createdAt': session[8]
	}