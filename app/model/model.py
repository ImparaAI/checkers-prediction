import numpy as np
from . import keras_model
from .hyperparameters import HyperParameters

class Model:

	def __init__(self, input_dimensions, output_dimensions, hyperparameters = None):
		self.input_dimensions = input_dimensions
		self.output_dimensions = output_dimensions
		self.hyperparameters = hyperparameters or HyperParameters()
		self.keras_model = keras_model.build(input_dimensions, output_dimensions, self.hyperparameters)

	def predict(self, prediction_input):
		output = self.keras_model.predict(prediction_input)

		return {
			'win_value': output[0][0][0],
			'action_probabilities': output[1].tolist()[0]
		}

	def train(self, inputs, win_values, action_probabilities):
		outputs = {
			'value_head': np.array(win_values),
			'policy_head': np.array(action_probabilities)
		}

		self.keras_model.fit(np.array(inputs), outputs)