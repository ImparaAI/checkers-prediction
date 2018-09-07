import unittest
import numpy as np
from app.game.game import Game
from .initial_state import build_initial_state
from app.model.input_state import build_input_state

class test_initial_state(unittest.TestCase):

	def test_initial_state(self):
		game = Game()

		np.testing.assert_array_equal(build_input_state(game), build_initial_state())
