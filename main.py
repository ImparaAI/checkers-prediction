import json
import click
from database import database
from app.prediction import predictor
from flask.cli import with_appcontext
from flask import Flask, request, jsonify
from app.training.session import restarter as training_session_restarter, fetcher as training_session_fetcher, runner as training_session_runner

app = Flask(__name__)

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

@click.command('database:initialize')
@with_appcontext
def initialize_database():
	if database.initialize():
		click.echo('Initialized the database.')
	else:
		click.echo('Database already initialized.')

@click.command('training_session:run')
@with_appcontext
def run_training_session():
	training_session_runner.run()

@click.command('training_session:test')
@with_appcontext
def test_training_session():
	training_session_restarter.restart({'secondsLimit': 500})
	training_session_runner.run()

app.teardown_appcontext(database.close_database)
app.cli.add_command(initialize_database)
app.cli.add_command(run_training_session)
app.cli.add_command(test_training_session)

if __name__ == '__main__':
	app.run(host = '0.0.0.0', port = 80, debug = True)