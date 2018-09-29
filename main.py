import json
import click
from database import database
from app.prediction import predictor
from flask.cli import with_appcontext
from flask import Flask, request, jsonify
from app.training.session import restarter as training_session_restarter, fetcher as training_session_fetcher

app = Flask(__name__)

@app.route("/predict", methods = ['GET'])
def predict():
	moves = json.loads(request.args.get('moves'))

	return jsonify({'prediction': predictor.predict(moves)})

@app.route("/training/session/create", methods = ['POST'])
def create_training_session():
	return jsonify({'id': training_session_restarter.restart(request.json)})

@app.route("/training/sessions", methods = ['GET'])
def get_training_sessions():
	return jsonify({'sessions': training_session_fetcher.get_all()})

@click.command('database:initialize')
@with_appcontext
def initialize_database_command():
	if database.initialize():
		click.echo('Initialized the database.')
	else:
		click.echo('Database already initialized.')

app.teardown_appcontext(database.close_database)
app.cli.add_command(initialize_database_command)

if __name__ == '__main__':
	app.run(host = '0.0.0.0', port = 80, debug = True)