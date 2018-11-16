import os
from flask import Flask
from . import routes, commands
from app.database import database

def create_app(config = None):
	app = Flask(__name__)

	load_config(app, config)
	prepare_instance_path(app)

	app.teardown_appcontext(database.close_database)
	routes.register(app)
	commands.register(app)

	return app

def load_config(app, config):
	app.config.from_mapping(
		SECRET_KEY = 'dev',
		DATABASE_FILE = os.path.join(app.instance_path, 'sqlite', 'prediction.db'),
		TRAINING_EPISODES_PER_BATCH = 100,
	)

	if config is None:
		app.config.from_pyfile('config.py', silent = True)
	else:
		app.config.update(config)

def prepare_instance_path(app):
	try:
		os.makedirs(app.instance_path)
	except OSError:
		pass