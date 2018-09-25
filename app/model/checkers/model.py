from app.model.model import Model
from app.training.session import fetcher as training_session_fetcher

def build(model_name = None):
	if not model_name:
		session = training_session_fetcher.get_latest_session()
		model_name = session['name']

	return Model('/data/' + model_name + '.h5', (34, 8, 4), 8 * 8 * 4)