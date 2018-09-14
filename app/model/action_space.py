import numpy as np

def get_action(index, game):
	actions = np.zeros(8 * game.board.height * game.board.width, dtype = np.int)
	actions[index] = 1

	actions = np.reshape(actions, (8, game.board.height, game.board.width))

	for direction, rows in enumerate(actions):
		for row, columns in enumerate(rows):
			for column, value in enumerate(columns):
				if value:
					return translate_action(game, direction, row, column)

def translate_action(game, direction, row, column):
	player_turn = game.whose_turn()
	translated_row = translate_row(row, game.board.height, player_turn)
	translated_column = translate_column(column, game.board.width, player_turn)

	from_position = game.board.position_layout[translated_row][translated_column]
	to_position = get_to_position(game, direction, translated_row, translated_column, player_turn)

	return [from_position, to_position]

def get_to_position(game, direction, from_row, from_column, player_turn):
	to_row_column = get_player_one_positions(from_row, from_column) if player_turn == 1 else get_player_two_positions(from_row, from_column)

	to_row = to_row_column[direction][0]
	to_column = to_row_column[direction][1]

	if (game.board.is_valid_row_and_column(to_row, to_column)):
		return game.board.position_layout[to_row][to_column]

def get_player_one_positions(row, column):
	return [
		get_south_east_row_column(row, column, 1),
		get_south_west_row_column(row, column, 1),
		get_north_east_row_column(row, column, 1),
		get_north_west_row_column(row, column, 1),
		get_south_east_row_column(row, column, 2),
		get_south_west_row_column(row, column, 2),
		get_north_east_row_column(row, column, 2),
		get_north_west_row_column(row, column, 2),
	]

def get_player_two_positions(row, column):
	return [
		get_north_west_row_column(row, column, 1),
		get_north_east_row_column(row, column, 1),
		get_south_west_row_column(row, column, 1),
		get_south_east_row_column(row, column, 1),
		get_north_west_row_column(row, column, 2),
		get_north_east_row_column(row, column, 2),
		get_south_west_row_column(row, column, 2),
		get_south_east_row_column(row, column, 2),
	]

def get_north_west_row_column(row, column, step_count):
	column = column if row % 2 == 0 else column - 1
	row = row - 1

	return [row, column] if step_count == 1 else get_north_west_row_column(row, column, step_count - 1)

def get_north_east_row_column(row, column, step_count):
	column = column + 1 if row % 2 == 0 else column
	row = row - 1

	return [row, column] if step_count == 1 else get_north_east_row_column(row, column, step_count - 1)

def get_south_west_row_column(row, column, step_count):
	column = column if row % 2 == 0 else column - 1
	row = row + 1

	return [row, column] if step_count == 1 else get_south_west_row_column(row, column, step_count - 1)

def get_south_east_row_column(row, column, step_count):
	column = column + 1 if row % 2 == 0 else column
	row = row + 1

	return [row, column] if step_count == 1 else get_south_east_row_column(row, column, step_count - 1)

def translate_row(row, board_height, player_turn):
	return board_height - 1 - row if player_turn == 1 else row;

def translate_column(column, board_width, player_turn):
	return board_width - 1 - column if player_turn == 1 else column;