import queue
from app.model.checkers import model as checkers_model

def predict(model_name, prediction_request_queue, prediction_response_queue):
	print('uhhhh')
	model = checkers_model.build(model_name)
	print('model created')
	while True:
		try:
			prediction_input = prediction_request_queue.get()
		except queue.Empty:
			continue

		if type(prediction_input).__name__ == 'ndarray':
			print('ok predicting')
			prediction = model.predict(prediction_input)
			prediction_request_queue.task_done()
			prediction_response_queue.put(prediction)
			prediction_response_queue.join()
		else:
			print('closing predictor')
			model.close()
			prediction_request_queue.task_done()
			return