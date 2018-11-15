import unittest
from app.prediction.predictor import predict

def test(app):
	with app.app_context():
		prediction = predict([])
		possible_moves = [[9, 13], [9, 14], [10, 14], [10, 15], [11, 15], [11, 16], [12, 16]]

		assert prediction in possible_moves