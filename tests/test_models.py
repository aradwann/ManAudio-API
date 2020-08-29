
from flask import current_app
from app import db, bcrypt
from app.models import User




def test_encode_auth_token(client):
    u = User(
        email='user@email.com',
        password='cat')
    db.session.add(u)
    db.session.commit()
    auth_token = u.encode_auth_token(u.id)
    assert isinstance(auth_token, bytes)
    assert u.decode_auth_token(auth_token) == 1