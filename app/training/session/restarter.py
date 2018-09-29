import datetime
from .storage import storage

def restart(session):
	storage.stop_active_sessions()

	return storage.create_new_session({
		'name': datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'),
		'episodeLimit': None,
		'secondsLimit': session.get('secondsLimit', 900)
	})