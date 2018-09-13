import unittest
import numpy as np

class BaseTest(unittest.TestCase):

	def build_initial_state(self):
		input_state = np.zeros((34, 8, 4), dtype=np.int)

		input_state[0] = [[0, 0, 0, 0],
		                  [0, 0, 0, 0],
		                  [0, 0, 0, 0],
		                  [0, 0, 0, 0],
		                  [0, 0, 0, 0],
		                  [1, 1, 1, 1],
		                  [1, 1, 1, 1],
		                  [1, 1, 1, 1]]

		input_state[16] = [[1, 1, 1, 1],
		                   [1, 1, 1, 1],
		                   [1, 1, 1, 1],
		                   [0, 0, 0, 0],
		                   [0, 0, 0, 0],
		                   [0, 0, 0, 0],
		                   [0, 0, 0, 0],
		                   [0, 0, 0, 0]]

		return input_state