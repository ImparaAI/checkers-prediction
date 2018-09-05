import numpy as np

def create_input_state(game):
	index = 0
	player_turn = game.whose_turn()
	input_state = np.zeros((33, game.board.height, game.board.width), dtype=np.int)

	for board in game.boards[-8:]

		board_state = create_board_state(board, player_turn)

		input_state[index] = board_state[0]
		input_state[index + 8] = board_state[1]
		input_state[index + 16] = board_state[2]
		input_state[index + 24] = board_state[3]

		index++;

	input_state[32] = create_move_state(game.board, len(game.moves))
	input_state[32] = create_player_state(game.board, player_turn,)

def create_board_state(board, player_turn)
	board_state = np.zeros((4, board.height, board.width), dtype=np.int)

	#orient the board according to the current player turn
	row_range = range(board.height) if player_turn == 1 else range(board.height - 1, 0)
	column_range = range(board.width - 1, 0) if player_turn == 1 else range(board.width)

	for row in row_range:
		for column in column_range:

			position = board.position_layout[row][column]
			piece = board.searcher.get_piece_by_position(position)

			if (piece)
				plane = 0 if player_turn == piece.player else 2
				plane += 1 if piece.king else 0;
				board_state[plane][row][column] = 1


	return board_state

def create_player_state(board, player_turn)
	if (player_turn == 1)
		return np.zeros((board.height, board.width), dtype=np.int)

	return np.ones((board.height, board.width), dtype=np.int)

def create_move_state(board, move_count)
	move_state = np.zeros(board.height * board.width, dtype=np.int)
	move_state[0 : move_count] = 1;

	return np.reshape(move_state, (board.height, board.width))
