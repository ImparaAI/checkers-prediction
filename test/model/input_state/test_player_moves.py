import numpy as np
from . import BaseTest
from checkers.game import Game
from app.model.checkers.input_builder import build as build_input_state

class test_player_moves(BaseTest):

	def test_one_move(self):
		game = Game()
		game.move([9, 14])

		np.testing.assert_array_equal(build_input_state(game), self.get_first_move_state())

	def test_two_moves(self):
		game = Game()
		game.move([9, 14])
		game.move([24, 20])

		np.testing.assert_array_equal(build_input_state(game), self.get_second_move_state())

	def get_first_move_state(self):
		input_state = self.build_initial_state()

		#set player 1 history  and new position
		input_state[17] = input_state[16]
		input_state[16] =[
			[1, 1, 1, 1],
			[1, 1, 1, 1],
			[0, 1, 1, 1],
			[0, 1, 0, 0],
			[0, 0, 0, 0],
			[0, 0, 0, 0],
			[0, 0, 0, 0],
			[0, 0, 0, 0]
		]

		#set new player 2 history
		input_state[1] = input_state[0]

		#player turn
		input_state[32] = np.ones((8, 4), dtype=np.int)

		#move count
		input_state[33][7][3] = 1

		return input_state

	def get_second_move_state(self):
		input_state = self.build_initial_state()

		#set new player 1 history
		input_state[2] = input_state[0]
		input_state[1] = [
			[0, 0, 0, 0],
			[0, 0, 0, 0],
			[0, 0, 0, 0],
			[0, 0, 0, 0],
			[0, 0, 1, 0],
			[1, 1, 1, 0],
			[1, 1, 1, 1],
			[1, 1, 1, 1]
		]
		input_state[0] = input_state[1]

		#set new player 2 positions
		input_state[18] = input_state[16]
		input_state[17] = input_state[16]
		input_state[16] = [
			[1, 1, 1, 1],
			[1, 1, 1, 1],
			[0, 1, 1, 1],
			[1, 0, 0, 0],
			[0, 0, 0, 0],
			[0, 0, 0, 0],
			[0, 0, 0, 0],
			[0, 0, 0, 0]
		]

		#two move count
		input_state[33][7][2] = 1
		input_state[33][7][3] = 0

		return input_state