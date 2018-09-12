from .hyperparameters import HyperParameters
from .keras_model_builder import KerasModelBuilder

class Model(object):

	def __init__(self, input_dimensions, output_dimensions, hyperparameters = None):
		self.input_dimensions = input_dimensions
		self.output_dimensions = output_dimensions
		self.hyperparameters = hyperparameters or HyperParameters()
		self.keras_model =  KerasModelBuilder(input_dimensions, output_dimensions, self.hyperparameters).build()

	def predict(self, prediction_input):
		return self.keras_model.predict(prediction_input)

	def train(self, inputs):
		return 'training is happening'