import pytest
from app import create_app

@pytest.fixture
def app():
	app = create_app({
		'TESTING': True,
	})

	return app

@pytest.fixture
def http(app):
	return app.test_client()

@pytest.fixture
def cli(app):
	return app.test_cli_runner()