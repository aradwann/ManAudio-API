import pytest
from app import create_app, db


@pytest.fixture()
def client():
    flask_app = create_app('testing')

    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    client = flask_app.test_client()

    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()
    db.create_all()

    yield client  # this is where the testing happens!

    db.drop_all()
    ctx.pop()
