from app import app
import pytest


@pytest.fixture
def app():
    my_app = app
    return my_app
