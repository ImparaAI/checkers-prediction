import numpy as np
from app.model.checkers.input_builder import build as build_input_state

def test_kings(game):
	boards = [game.board]

	for move in get_moves():
		game.move(move)
		boards.append(game.board)

	np.testing.assert_array_equal(build_input_state(game, boards), build_expected())

def get_moves():
	return [[10, 15], [23, 19], [15, 18], [22, 15], [11, 18], [19, 15], [6, 10], [15, 6], [1, 10], [24, 19], [10, 15], [19, 10], [7, 14],
	        [21, 17], [14, 21], [25, 22], [18, 25], [29, 22], [9, 14], [30, 25], [21, 30], [27, 23], [12, 16], [22, 18], [14, 17], [18, 14],
	        [17, 21], [14, 10], [2, 6], [10, 1], [30, 25]];

def build_expected():
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
		[[0, 0, 0, 0],
		 [0, 0, 0, 0],
		 [0, 0, 0, 0],
		 [0, 0, 0, 0],
		 [0, 0, 0, 0],
		 [0, 0, 0, 0],
		 [0, 0, 0, 1],
		 [1, 1, 1, 1]],
	]