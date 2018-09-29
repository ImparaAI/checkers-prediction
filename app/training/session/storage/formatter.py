import datetime

def format_many(sessions):
	pass

def format(session):
	date_format = '%Y-%m-%d %H:%M:%S'

	print(session)

	return {
		'startTime': datetime.datetime.strptime(date, date_format)
	}