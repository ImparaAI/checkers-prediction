import numpy as np
from . import build_initial_state
from app.model.checkers.input_builder import build as build_input_state

def test_initial_state(game):
	np.testing.assert_array_equal(build_input_state(game, [game.board]), build_initial_state())