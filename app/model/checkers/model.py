import os
from app.model.model import Model
from app.training.session import fetcher as training_session_fetcher

def build(model_name = None):
	session = training_session_fetcher.get_latest_session() if not model_name else None
	filename = None

	if session or model_name:
		directory = os.path.join(os.path.dirname(__file__), 'data/weights/')

		if not os.path.exists(directory):
			os.makedirs(directory)

		filename = directory + (model_name if model_name else session['name']) + '.h5'

	return Model(filename, (34, 8, 4), 8 * 8 * 4)