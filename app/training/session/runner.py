import time
from .storage import storage
from app.training import trainer

def run():
	session = storage.get_next_session()

	if not session:
		return

	start_time = time.time()
	storage.activate(session['id'])
	episodes_per_training = 30

	while not time_limit_reached(start_time, session) and storage.is_active(session['id']):
		trainer.train(session['name'], episodes_per_training)
		storage.boost_episode_count(session['id'], episodes_per_training)

	storage.finish(session['id'])

def time_limit_reached(start_time, session):
	session_limit = session['secondsLimit']
	time_elapsed = time.time() - start_time

	return False if (session_limit == None) or (time_elapsed < session_limit) else True