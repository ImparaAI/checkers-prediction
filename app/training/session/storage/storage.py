fake_session = {
	'id': 1,
	'name': 'init',
	'secondsLimit': 2000
}

def stop_active_sessions():
	pass

def create_new_session():
	pass

def get_next_session():
	return fake_session

def activate(id, time):
	pass

def is_active(id):
	return True

def deactivate_session(id, time):
	pass

def get_latest_session():
	return fake_session

def get_all():
	return [fake_session]
