from .storage import storage

def restart(request):
	storage.stop_active_sessions()

	return storage.create_new_session(request)