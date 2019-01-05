import os
from app.model.model import Model
from app.training.session import fetcher as training_session_fetcher

def build(model_name = None):
	session = training_session_fetcher.get_latest_session() if not model_name else None
	weights_path = None

	if session or model_name:
		filename = (model_name if model_name else session['name']) + '.h5'
		weights_path = os.path.join(os.path.dirname(__file__), 'data/' + filename)

	return Model(weights_path, (34, 8, 4), 8 * 8 * 4)