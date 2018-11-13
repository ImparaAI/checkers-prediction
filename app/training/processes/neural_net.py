import queue
import random
from app.model.checkers import model as checkers_model

model = None
lessons = []
max_batch_size = 1024
preferred_batch_count = 20

def run(model_name, prediction_requests, lesson_pipes, halt_signal):
	print('neural net starting')
	global model
	model = checkers_model.build(model_name)
	print('neural net model loaded')

	while True:
		if halt_signal.value:
			train()
			model.close()
			return

		for prediction_request in prediction_requests:
			if prediction_request.needs_response():
				prediction = model.predict(prediction_request.get_input())
				prediction_request.set_response(prediction)

		gather_new_lessons(lesson_pipes)

def gather_new_lessons(lesson_pipes):
	for pipe in lesson_pipes:
		if pipe.poll():
			lessons.extend(pipe.recv())

def train():
	batch_size = min(max_batch_size, len(lessons) // preferred_batch_count)
	random.shuffle(lessons)

	while len(lessons):
		inputs, win_values, action_probabilities = build_training_values(batch_size)
		model.train(inputs, win_values, action_probabilities)

	model.save()

def build_training_values(batch_size):
	inputs, win_values, action_probabilities = ([], [], [])

	for x in range(1, batch_size):
		if len(lessons):
			lesson = lessons.pop()
			inputs.append(lesson.input)
			win_values.append(lesson.win_value)
			action_probabilities.append(lesson.action_probabilities)

	return inputs, win_values, action_probabilities