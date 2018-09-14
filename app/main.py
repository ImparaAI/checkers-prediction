import json
from prediction import predictor
from flask import Flask, request, jsonify
from training.session import restarter as training_session_restarter

app = Flask(__name__)

@app.route("/train", methods=['POST'])
def train():
	return jsonify({'id': training_session_restarter.restart(request.json)})

@app.route("/predict", methods=['GET'])
def predict():
	moves = json.loads(request.args.get('moves'))

	return jsonify({'prediction': predictor.predict(moves)})

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80, debug=True)