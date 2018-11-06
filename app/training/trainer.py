import random
import multiprocessing
from .predictor import predict
from .game_player import play_games
from multiprocessing.managers import BaseManager
from .prediction_request import PredictionRequest
from app.model.checkers import model as checkers_model

def train(model_name, episodes = 5):
	Trainer(model_name).train(episodes)

class Trainer:

	def __init__(self, model_name):
		self.model_name = model_name
		self.lessons = []
		self.max_batch_size = 1024
		self.preferred_batch_count = 20

	def train(self, episode_count):
		halt_signal = multiprocessing.Value('i', 0)
		lesson_pipes = self.build_lesson_pipes(self.get_player_process_count())
		prediction_process, game_player_processes = self.create_processes(lesson_pipes, halt_signal, episode_count)

		prediction_process.start()

		[process.start() for process in game_player_processes]
		print('all processes started')

		[self.lessons.extend(pipe[0].recv()) for pipe in lesson_pipes]
		halt_signal.value = 1

		print('all processes completed')

		self.update_model()
		print('done')

	def create_processes(self, lesson_pipes, halt_signal, episode_count):
		player_process_count = self.get_player_process_count()
		prediction_requests = self.build_prediction_requests(player_process_count)
		prediction_process = multiprocessing.Process(target = predict, args = (self.model_name, prediction_requests, halt_signal))
		game_player_processes = []
		episode_counts = self.build_episode_counts(episode_count, player_process_count)

		for i in range(player_process_count):
			game_player_processes.append(multiprocessing.Process(target = play_games, args = (episode_counts[i - 1], lesson_pipes[i - 1][1], prediction_requests[i - 1])))

		return prediction_process, game_player_processes


	def get_player_process_count(self):
		return multiprocessing.cpu_count() - 1

	def build_lesson_pipes(self, count):
		lesson_pipes = []

		for i in range(count):
			parent_lesson_connection, child_lesson_connection = multiprocessing.Pipe()
			lesson_pipes.append([parent_lesson_connection, child_lesson_connection])

		return lesson_pipes

	def build_episode_counts(self, episode_count, process_count):
		counts = [episode_count // process_count] * process_count
		left_over = episode_count - sum(counts)

		for i in range(left_over):
			counts[i - 1] += 1

		return counts

	def build_prediction_requests(self, process_count):
		BaseManager.register('PredictionRequest', PredictionRequest)
		manager = BaseManager()
		manager.start()

		return list(map(lambda i: manager.PredictionRequest(), range(process_count)))

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