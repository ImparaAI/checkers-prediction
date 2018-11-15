import json
from flask import request, jsonify
from app.prediction import predictor
from app.training.session import restarter as training_session_restarter, fetcher as training_session_fetcher

def register(app):
	@app.route("/predict", methods = ['GET'])
	def predict():
		moves = json.loads(request.args.get('moves'))

		try:
			move = predictor.predict(moves)
		except ValueError as e:
			return str(e), 400

		return jsonify({'prediction': move})

	@app.route("/training/session", methods = ['POST'])
	def create_training_session():
		session = request.get_json()
		return jsonify({'id': training_session_restarter.restart(session)})

	@app.route("/training/sessions", methods = ['GET'])
	def get_training_sessions():
		return jsonify({'sessions': training_session_fetcher.get_all()})