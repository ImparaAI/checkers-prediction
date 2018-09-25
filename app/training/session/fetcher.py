from .storage import storage

def get_latest_session():
	return storage.get_latest_session()