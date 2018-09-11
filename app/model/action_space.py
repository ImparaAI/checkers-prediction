import numpy as np

def get_available_actions

def get_action(index, game):
	player_turn = game.whose_turn()
	actions = np.zeros(game.board.height * game.board.length, dtype = np.int)
	actions[index] = 1

	actions = np.reshape(actions, (8, game.board.height, game.board.length))

	for plane, rows in actions:
		for row, columns in rows:
			for column, value in columns:
				if value:
					from_position = board.position_layout[row][column]
					to_position = get_to_position(plane, row, column)

					return build(plane, row, column)

def build(plane, row, column)
	return [from_position, to_position]

def get_to_position(plane, row, column)
	relative_moves = [
		[-1, -1],
		[-1,  1],
		[ 1, -1],
		[ 1,  1],
		[-2, -2],
		[-2,  2],
		[ 2, -2],
		[ 2,  2],
	]

	row += relative_moves(plane)[0]
	column += relative_moves(plane)[1]

	if (board.is_valid_row_column):
		return board.position_layout[row][column]