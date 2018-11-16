import pytest

def test(app, http, cli):
	check_sessions(http, [])

	restart_training(http, {'secondsLimit': 1})

	check_sessions(http, [{
		'id': 1,
		'secondsLimit': 1,
		'episodeCount': 0,
	}])

	response = cli.invoke(args = ['training_session:run'])

	check_sessions(http, [{
		'id': 1,
		'secondsLimit': 1,
		'episodeCount': 1,
	}])

	restart_training(http, {'secondsLimit': 1})

	check_sessions(http, [
		{
			'id': 2,
			'secondsLimit': 1,
			'episodeCount': 0,
		},
		{
			'id': 1,
			'secondsLimit': 1,
			'episodeCount': 1,
		},
	])

def check_sessions(http, expected_sessions):
	response = http.get('/training/sessions')

	assert response.status_code == 200
	assert response.is_json

	response_data = response.get_json()

	assert 'sessions' in response_data

	if not expected_sessions:
		assert response_data['sessions'] == expected_sessions
		return

	assert len(expected_sessions) == len(response_data['sessions'])

	for i, expected_session in enumerate(expected_sessions):
		for key, value in expected_session.items():
			assert expected_session[key] == response_data['sessions'][i][key]

def restart_training(http, session_data):
	http.post('/training/session', json = session_data)