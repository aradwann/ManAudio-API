import pytest
from app import create_app, db
from app.models import User


@pytest.fixture()
def client():
    flask_app = create_app('testing')

    # Flask provides a way to test your app
    # by exposing the Werkzeug test Client
    # and handling the context locals for you.
    client = flask_app.test_client()

    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()
    db.create_all()

    yield client  # this is where the testing happens!

    db.drop_all()
    ctx.pop()


@pytest.fixture()
def user():
    user = User(
        email='joe@gmail.com',
        password='123456'
    )
    db.session.add(user)
    db.session.commit()
    return user
