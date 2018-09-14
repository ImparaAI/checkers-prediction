from .hyperparameters import HyperParameters
from .keras_model_builder import KerasModelBuilder

class Model:

	def __init__(self, input_dimensions, output_dimensions, hyperparameters = None):
		self.input_dimensions = input_dimensions
		self.output_dimensions = output_dimensions
		self.hyperparameters = hyperparameters or HyperParameters()
		self.keras_model =  KerasModelBuilder(input_dimensions, output_dimensions, self.hyperparameters).build()

	def predict(self, prediction_input):
		output = self.keras_model.predict(prediction_input)

		return {
			'win_value': output[0][0][0],
			'action_probabilities': output[1].tolist()[0]
		}

	def train(self, inputs):
		return 'training is happening'