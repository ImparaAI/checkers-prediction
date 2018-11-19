import numpy as np
from . import build_initial_state, play_moves
from app.model.checkers.input_builder import build as build_input_state

def test_one_move(game):
	boards = play_moves(game, [[9, 14]])

	np.testing.assert_array_equal(build_input_state(game, boards), get_first_move_state())

def test_two_moves(game):
	boards = play_moves(game, [[9, 14], [24, 20]])

	np.testing.assert_array_equal(build_input_state(game, boards), get_second_move_state())

def get_first_move_state():
	input_state = build_initial_state()

	#set player 1 history  and new position
	input_state[17] = input_state[16]
	input_state[16] = [
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
	input_state[32] = np.ones((8, 4), dtype = np.int)

	#one move without capture
	input_state[33][7][3] = 1

	return input_state

def get_second_move_state():
	input_state = build_initial_state()

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

	#two moves without capture
	input_state[33][7][2] = 1
	input_state[33][7][3] = 0

	return input_state