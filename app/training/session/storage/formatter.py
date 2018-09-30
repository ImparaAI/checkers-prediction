import datetime

def format_many(sessions):
	return list(map(lambda session: format(session), sessions))

def format(session):
	return {
		'id': session[0],
		'name': session[1],
		'episodeCount': session[2],
		'episodeLimit': session[3],
		'secondsLimit': session[4],
		'deactivated': bool(session[5]),
		'startTime': format_time(session[6]),
		'endTime': format_time(session[7]),
		'createdAt': format_time(session[8])
	}

def format_time(value):
	if not value:
		return value

	return value.strftime('%Y-%m-%d %H:%M:%S')