import queue
from app.model.checkers import model as checkers_model

def predict(model_name, prediction_requests, halt_signal):
	print('predictor starting')
	model = checkers_model.build(model_name)
	print('nn model loaded')

	while True:
		if halt_signal.value:
			print('exiting predictor')
			model.close()
			return

		for prediction_request in prediction_requests:
			if prediction_request.needs_response():
				prediction = model.predict(prediction_request.get_input())
				prediction_request.set_response(prediction)