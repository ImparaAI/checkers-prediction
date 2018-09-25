import time
from .storage import storage
from app.training import trainer

def run():
	session = storage.get_next_session()

	if not session:
		return

	start_time = time.time()
	storage.activate(session['id'], start_time)

	while not time_limit_reached(start_time, session) and storage.is_active(session['id']):
		trainer.train(session['name'])

	storage.deactivate_session(session['id'], time.time())

def time_limit_reached(start_time, session):
	session_limit = session['secondsLimit']
	time_elapsed = time.time() - start_time

	return False if (session_limit == None) or (time_elapsed < session_limit) else True