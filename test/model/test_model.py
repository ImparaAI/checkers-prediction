import unittest
import numpy as np
from app.game.game import Game
from app.model.model import Model
from app.model.input_state import build_input_state

class test_model(unittest.TestCase):

	def test_model(self):

		game = Game()

		reg_const = 0.0001
		learning_rate = 0.1
		input_dimensions = (34, 8, 4) #(2, 6, 7)
		output_dimensions = 8 * 8 * 4 #42

		nn = Model(reg_const, learning_rate, input_dimensions, output_dimensions)


		nn.model.set_weights(nn.model.get_weights())


		wow = nn.predict(np.array([build_input_state(game)]))

		print(wow)