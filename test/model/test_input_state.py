import unittest
import numpy as np
from app.game.game import Game
from app.model.input_state import build_input_state

class test_input_state(unittest.TestCase):

	def test_inital_position(self):
		game = Game()

		input_state = self.build_inital_state()

		np.testing.assert_array_equal(build_input_state(game), input_state)

	def test_one_move(self):
		game = Game()
		game.move([9, 14])

		input_state = self.build_inital_state()

		#set new player 1 positions
		input_state[17] = input_state[16]
		input_state[16][2][0] = 0
		input_state[16][3][1] = 1

		#set new player 2 positions
		input_state[1] = input_state[0]

		#player turn
		input_state[32] = np.ones((8, 4), dtype=np.int)

		#move count
		input_state[33][0][0] = 1

		np.testing.assert_array_equal(build_input_state(game), input_state)

	def test_two_moves(self):
		game = Game()
		game.move([9, 14])
		game.move([24, 20])

		input_state = self.build_inital_state()

		#set new player 1 positions
		input_state[2] = input_state[0]
		input_state[1] = input_state[0]
		input_state[1][5][3] = 0
		input_state[1][4][2] = 1
		input_state[0] = input_state[1]

		#set new player 2 positions
		input_state[18] = input_state[16]
		input_state[17] = input_state[16]
		input_state[16] = input_state[16]
		input_state[16][2][0] = 0
		input_state[16][3][0] = 1

		#two move count
		input_state[33][0][0] = 1
		input_state[33][0][1] = 1

		np.testing.assert_array_equal(build_input_state(game), input_state)

	def test_kings(self):
		game = Game()
		moves = [[10, 15],[23, 19],[15, 18],[22, 15],[11, 18],[19, 15],[6, 10],[15, 6],[1, 10],[24, 19],[10, 15],[19, 10],[7, 14],[21, 17],[14, 21],[25, 22],[18, 25],[29, 22],[9, 14],[30, 25],[21, 30],[27, 23],[12, 16],[22, 18],[14, 17],[18, 14],[17, 21],[14, 10],[2, 6],[10, 1],[30, 25]]

		for move in moves:
			game.move(move)

		np.testing.assert_array_equal(build_input_state(game), self.build_king_state())

	def build_inital_state(self):
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

	def build_king_state(self):
		return [
			#man history 1
			[[0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 1, 0],
			 [0, 1, 0, 1],
			 [0, 0, 1, 1]],
			#man history 2
			[[0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 1, 0],
			 [0, 1, 0, 1],
			 [0, 0, 1, 1]],
			#man history 3
			[[0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 1, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 1, 0],
			 [0, 1, 0, 1],
			 [0, 0, 1, 1]],
			#man history 4
			[[0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 1, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 1, 0],
			 [0, 1, 0, 1],
			 [0, 0, 1, 1]],
			#man history 5
			[[0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 1, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 1, 0],
			 [0, 1, 0, 1],
			 [0, 0, 1, 1]],
			#man history 6
			[[0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 1, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 1, 0],
			 [0, 1, 0, 1],
			 [0, 0, 1, 1]],
			#man history 7
			[[0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 1, 0, 0],
			 [0, 0, 1, 0],
			 [0, 1, 0, 1],
			 [0, 0, 1, 1]],
			#man history 8
			[[0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 1, 0, 0],
			 [0, 0, 1, 0],
			 [0, 1, 0, 1],
			 [0, 0, 1, 1]],
			#king history 1
			[[1, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0]],
			#king history 2
			[[1, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0]],
			#king history 3
			[[0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0]],
			#king history 4
			[[0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0]],
			#king history 5
			[[0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0]],
			#king history 6
			[[0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0]],
			#king history 7
			[[0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0]],
			#king history 8
			[[0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0]],
			#opponent man history 1
			[[0, 0, 1, 1],
			 [1, 0, 0, 1],
			 [0, 0, 0, 0],
			 [0, 0, 0, 1],
			 [0, 0, 0, 0],
			 [1, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0]],
			#opponent man history 2
			[[0, 0, 1, 1],
			 [1, 0, 0, 1],
			 [0, 0, 0, 0],
			 [0, 0, 0, 1],
			 [0, 0, 0, 0],
			 [1, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0]],
			#opponent man history 3
			[[0, 0, 1, 1],
			 [1, 1, 0, 1],
			 [0, 0, 0, 0],
			 [0, 0, 0, 1],
			 [0, 0, 0, 0],
			 [1, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0]],
			#opponent man history 4
			[[0, 1, 1, 1],
			 [1, 0, 0, 1],
			 [0, 0, 0, 0],
			 [0, 0, 0, 1],
			 [0, 0, 0, 0],
			 [1, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0]],
			#opponent man history 5
			[[0, 1, 1, 1],
			 [1, 0, 0, 1],
			 [0, 0, 0, 0],
			 [0, 0, 0, 1],
			 [0, 0, 0, 0],
			 [1, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0]],
			#opponent man history 6
			[[0, 1, 1, 1],
			 [1, 0, 0, 1],
			 [0, 0, 0, 0],
			 [0, 0, 0, 1],
			 [1, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0]],
			#opponent man history 7
			[[0, 1, 1, 1],
			 [1, 0, 0, 1],
			 [0, 0, 0, 0],
			 [0, 0, 0, 1],
			 [1, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0]],
			#opponent man history 8
			[[0, 1, 1, 1],
			 [1, 0, 0, 1],
			 [0, 0, 0, 0],
			 [0, 1, 0, 1],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0]],
			#opponent king history 1
			[[0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [1, 0, 0, 0],
			 [0, 0, 0, 0]],
			#opponent king history 2
			[[0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 1, 0, 0]],
			#opponent king history 3
			[[0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 1, 0, 0]],
			#opponent king history 4
			[[0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 1, 0, 0]],
			#opponent king history 5
			[[0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 1, 0, 0]],
			#opponent king history 6
			[[0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 1, 0, 0]],
			#opponent king history 7
			[[0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 1, 0, 0]],
			#opponent king history 8
			[[0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 0, 0, 0],
			 [0, 1, 0, 0]],
			#player 2 turn
			[[1, 1, 1, 1],
			 [1, 1, 1, 1],
			 [1, 1, 1, 1],
			 [1, 1, 1, 1],
			 [1, 1, 1, 1],
			 [1, 1, 1, 1],
			 [1, 1, 1, 1],
			 [1, 1, 1, 1]],
			#move count
			[[1, 1, 1, 1],
			 [1, 1, 1, 1],
			 [1, 1, 1, 1],
			 [1, 1, 1, 1],
			 [1, 1, 1, 1],
			 [1, 1, 1, 1],
			 [1, 1, 1, 1],
			 [1, 1, 1, 0]],
		]