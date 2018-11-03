import random
import multiprocessing
from .predictor import predict
from .game_player import play_game
from app.model.checkers import model as checkers_model


import time

def train(model_name, episodes = 5):
	Trainer(model_name).train(episodes)

class Trainer:

	def __init__(self, model_name):
		self.model_name = model_name
		self.lessons = []
		self.max_batch_size = 1024
		self.preferred_batch_count = 20

	def train(self, episodes):
		lesson_queue = multiprocessing.Queue()
		prediction_request_queue = multiprocessing.JoinableQueue()
		prediction_response_queue = multiprocessing.JoinableQueue()
		prediction_process = multiprocessing.Process(target = predict, args = (self.model_name, prediction_request_queue, prediction_response_queue))
		prediction_process.start()
		processes = []

		for i in range(episodes):
			processes.append(multiprocessing.Process(target = play_game, args = (lesson_queue, prediction_request_queue, prediction_response_queue)))
			processes[-1].start()
		print('started')

		live_processes = list(processes)

		print('doing')
		# while live_processes:
		# 	print(processes[-1].is_alive())
		# 	live_processes = [process for process in live_processes if process.is_alive()]
		# 	time.sleep(1)

		for process in processes:
			process.join()
		print('finished')

		prediction_request_queue.put(None)
		prediction_request_queue.join()

		print('hey there')
		while not lesson_queue.empty():
			self.lessons.append(lesson_queue.get())
		print('alrighty')
		self.update_model()

	def update_model(self):
		model = checkers_model.build(self.model_name)
		batch_size = min(self.max_batch_size, len(self.lessons) // self.preferred_batch_count)
		random.shuffle(self.lessons)

		while len(self.lessons):
			inputs, win_values, action_probabilities = self.build_training_values(batch_size)
			model.train(inputs, win_values, action_probabilities)

		model.save()
		model.close()

	def build_training_values(self, batch_size):
		inputs, win_values, action_probabilities = ([], [], [])

		for x in range(1, batch_size):
			if len(self.lessons):
				lesson = self.lessons.pop()
				inputs.append(lesson.input)
				win_values.append(lesson.win_value)
				action_probabilities.append(lesson.action_probabilities)

		return inputs, win_values, action_probabilities