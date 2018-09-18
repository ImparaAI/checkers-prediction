import numpy as np
from . import BaseTest
from checkers.game import Game
from app.model.checkers.input_builder import build as build_input_state

class test_initial_state(BaseTest):

	def test_initial_state(self):
		game = Game()

		np.testing.assert_array_equal(build_input_state(game), self.build_initial_state())
