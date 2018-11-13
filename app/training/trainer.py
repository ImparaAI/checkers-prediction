import multiprocessing
from .processes.game_playing import play_games
from multiprocessing.managers import BaseManager
from .prediction_request import PredictionRequest
from app.model.checkers import model as checkers_model
from .processes.neural_net import run as run_neural_net

def train(model_name, episodes = 5):
	Trainer(model_name).train(episodes)

class Trainer:

	def __init__(self, model_name):
		self.model_name = model_name
		self.lessons = []

	def train(self, episode_count):
		print('training', episode_count, 'new episodes')
		halt_signal = multiprocessing.Value('i', 0)
		neural_net_process, game_player_processes = self.create_processes(halt_signal, episode_count)

		neural_net_process.start()

		[process.start() for process in game_player_processes]
		[process.join() for process in game_player_processes]

		halt_signal.value = 1

		neural_net_process.join()
		print('episode training complete')

	def create_processes(self, halt_signal, episode_count):
		player_process_count = self.get_game_playing_process_count()
		prediction_requests = self.build_prediction_requests(player_process_count)
		parent_lesson_pipes, child_lesson_pipes = self.build_lesson_pipes(player_process_count)
		neural_net_process = multiprocessing.Process(target = run_neural_net, args = (self.model_name, prediction_requests, parent_lesson_pipes, halt_signal))
		game_player_processes = []
		episode_counts = self.build_episode_counts(episode_count, player_process_count)

		for i in range(player_process_count):
			game_player_processes.append(multiprocessing.Process(target = play_games, args = (episode_counts[i - 1], prediction_requests[i - 1], child_lesson_pipes[i - 1])))

		return neural_net_process, game_player_processes


	def get_game_playing_process_count(self):
		return multiprocessing.cpu_count() - 1

	def build_lesson_pipes(self, count):
		parents = []
		children = []

		for i in range(count):
			parent, child = multiprocessing.Pipe()
			parents.append(parent)
			children.append(child)

		return parents, children

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