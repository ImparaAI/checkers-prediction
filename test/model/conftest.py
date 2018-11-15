import pytest
from checkers.game import Game

@pytest.fixture
def game():
	return Game()