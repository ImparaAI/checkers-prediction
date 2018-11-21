import click
from app.database import database
from flask.cli import with_appcontext
from app.training.session import restarter as training_session_restarter, runner as training_session_runner

def register(app):
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

	app.cli.add_command(initialize_database)
	app.cli.add_command(run_training_session)
	app.cli.add_command(test_training_session)