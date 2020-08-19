import pytest
from app import create_app


@pytest.fixture()
def test_client():
    flask_app = create_app('testing')

    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = flask_app.test_client()

    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client  # this is where the testing happens!

    ctx.pop()

"""
@pytest.fixture()
def init_database(scope='session'):
    # Create the database and the database table
    db.create_all()

    yield db  # this is where the testing happens!

    db.drop_all()
"""