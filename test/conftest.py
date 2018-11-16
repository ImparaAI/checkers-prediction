import os
import pytest
import tempfile
from app import create_app

@pytest.fixture
def app():
	db_file_descriptor, db_file_path = tempfile.mkstemp()

	app = create_app({
		'TESTING': True,
		'DATABASE_FILE': db_file_path,
		'TRAINING_EPISODES_PER_BATCH': 1,
	})

	with app.app_context():
		app.test_cli_runner().invoke(args = ['database:initialize'])

	yield app

	os.close(db_file_descriptor)
	os.unlink(db_file_path)

@pytest.fixture
def http(app):
	return app.test_client()

@pytest.fixture
def cli(app):
	return app.test_cli_runner()