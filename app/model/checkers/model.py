import os
from app.model.model import Model
from app.training.session import fetcher as training_session_fetcher

def build(model_name = None):
	session = training_session_fetcher.get_latest_session() if not model_name else ''
	filename = os.path.join(os.path.dirname(__file__), 'data/' + session['name'] + '.h5') if session else None

	return Model(filename, (34, 8, 4), 8 * 8 * 4)