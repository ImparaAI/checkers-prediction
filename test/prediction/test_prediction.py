import unittest
from app.prediction.predictor import predict

class test_prediction(unittest.TestCase):

	def test(self):
		prediction = predict([], 1)
		possible_moves = [[9, 13], [9, 14], [10, 14], [10, 15], [11, 15], [11, 16], [12, 16]]

		self.assertTrue(prediction in possible_moves)