import json
import pytest

@pytest.mark.parametrize("input,possible_moves", [
	([], [[9, 13], [9, 14], [10, 14], [10, 15], [11, 15], [11, 16], [12, 16]]),
	([[9, 13]], [[21, 17], [22, 17], [22, 18], [23, 18], [23, 19], [24, 19], [24, 20]]),
])
def test_new_game(http, input, possible_moves):
	response = request_with_moves(http, input)
	response_data = json.loads(response.data.decode('utf-8'))

	assert 'prediction' in response_data
	assert response_data['prediction'] in possible_moves

@pytest.mark.parametrize("moves", [
	#game won
	([[10, 14], [23, 18], [14, 23], [26, 19], [11, 15], [19, 10], [6, 15], [22, 18], [15, 22], [25, 18], [9, 13], [21, 17], [13, 22], [31, 26], [22, 31], [24, 19],
		[31, 24], [24, 15], [15, 22], [29, 25], [22, 29], [30, 25], [29, 22], [28, 24], [12, 16], [32, 27], [16, 20], [27, 23], [20, 27], [23, 18], [22, 15]]),
	#no legal moves
	([[11, 15], [22, 18], [15, 22], [25, 18], [12, 16], [18, 14], [9, 18], [23, 14], [10, 17], [21, 14], [5, 9], [14, 5], [6, 9], [29, 25], [9, 13], [25, 22],
		[2, 6], [22, 18], [13, 17], [27, 23], [17, 21], [24, 19], [8, 12], [30, 25], [21, 30], [28, 24], [4, 8], [18, 14], [6, 10], [32, 27], [10, 17], [23, 18],
		[16, 23], [23, 32], [24, 19], [30, 23], [23, 14], [31, 27], [32, 23], [23, 16]]),
	#draw
	([[10, 14], [22, 17], [9, 13], [17, 10], [7, 14], [25, 22], [6, 10], [29, 25], [1, 6], [22, 18], [6, 9], [24, 19], [2, 6], [28, 24], [11, 16], [24, 20], [8, 11],
		[32, 28], [4, 8], [27, 24], [3, 7], [31, 27], [13, 17], [25, 22], [9, 13], [18, 9], [9, 2], [10, 14], [22, 18], [5, 9], [19, 15], [16, 19], [23, 16], [12, 19],
		[30, 25], [14, 23], [23, 32], [21, 14], [14, 5], [11, 18], [2, 11], [11, 4], [19, 23], [26, 19], [13, 17], [25, 21], [17, 22], [21, 17], [22, 25], [17, 14],
		[18, 22], [5, 1], [22, 26], [4, 8], [26, 31], [19, 15], [25, 30], [8, 11], [31, 26], [1, 6], [26, 23], [24, 19], [23, 16], [16, 7], [14, 10], [7, 14], [15, 10],
		[14, 7], [28, 24], [32, 28], [20, 16], [28, 19], [19, 12], [6, 9], [7, 10], [9, 13], [10, 7], [13, 9], [7, 3], [9, 6], [3, 7], [6, 1], [7, 11], [1, 6], [11, 8],
		[6, 9], [8, 11], [9, 6], [11, 8], [6, 9], [8, 11], [9, 6], [11, 8], [6, 9], [8, 11], [9, 6], [11, 8], [6, 9], [8, 11], [9, 6], [11, 8], [6, 9], [8, 11], [9, 6],
		[11, 8], [6, 9], [8, 11], [9, 6], [11, 8], [6, 9], [8, 11], [9, 6], [11, 8]]),
])
def test_game_over(http, moves):
	response = request_with_moves(http, moves)

	assert response.status_code == 400
	assert response.data.decode('utf-8') == 'The game is already over.'

@pytest.mark.parametrize("input", [
	(None), ('Foo'), (5), ({}),
])
def test_malformed_moves_list(http, input):
	check_failure(request_with_moves(http, input), 'The input needs to be a json list of moves (ex: moves="[[9, 13], ...]").')

@pytest.mark.parametrize("input", [
	(['foo', 5]), ([[5, 3]]), ([[], []]), ([{}, {}]),
])
def test_bad_moves(http, input):
	check_failure(request_with_moves(http, input), 'The provided move is not possible')

def request(http, data):
	return http.get('/predict', query_string = data)

def request_with_moves(http, moves):
	return request(http, {'moves': json.dumps(moves)})

def check_failure(response, message):
	assert response.status_code == 400
	assert response.data.decode('utf-8') == message