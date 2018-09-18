import unittest
import numpy as np
from checkers.game import Game
from app.model.model import Model
from app.prediction.predictor import predict
from app.model.checkers.input_builder import build as build_input_state

class test_model(unittest.TestCase):

	def test_model(self):
		game = Game()

		input_dimensions = (34, 8, 4)
		output_dimensions = 8 * 8 * 4

		model = Model(input_dimensions, output_dimensions)

		prediction = model.predict(np.array([build_input_state(game)]))