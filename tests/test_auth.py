import json
from app.models import User
from app import db


def test_registration(client):
    """ Test for user registration """

    response = client.post(
        '/auth/register',
        data=json.dumps(dict(
            email='joe@gmail.com',
            password='123456'
        )),
        content_type='application/json'
    )
    data = json.loads(response.data.decode())
    assert (data['status'] == 'success')
    assert (data['message'] == 'Successfully registered.')
    assert (data['auth_token'])
    assert (response.content_type == 'application/json')
    assert (response.status_code == 201)


def test_registered_with_already_registered_user(client):
    """ Test registration with already registered email"""
    user = User(
        email='joe@gmail.com',
        password='test'
    )
    db.session.add(user)
    db.session.commit()

    response = client.post(
        '/auth/register',
        data=json.dumps(dict(
            email='joe@gmail.com',
            password='123456'
        )),
        content_type='application/json'
    )
    data = json.loads(response.data.decode())
    assert (data['status'] == 'fail')
    assert (
        data['message'] == 'User already exists. Please Log in.')
    assert (response.content_type == 'application/json')
    assert (response.status_code == 202)


def test_registered_user_login_correct_password(client):
    """Test registered user login"""
    user = User(
        email='joe@gmail.com',
        password='test'
    )
    db.session.add(user)
    db.session.commit()
    response = client.post(
        '/auth/login',
        data=json.dumps(dict(
            email='joe@gmail.com',
            password='test'
        )),
        content_type='application/json')
    data = json.loads(response.data.decode())
    assert data['status'] == 'success'
    assert data['message'] == 'Successfully logged in.'
    assert data['auth_token']
    assert response.content_type == 'application/json'
    assert response.status_code == 200


def test_registered_user_login_wrong_password(client):
    """Test registered user login"""
    user = User(
        email='joe@gmail.com',
        password='test'
    )
    db.session.add(user)
    db.session.commit()
    response = client.post(
        '/auth/login',
        data=json.dumps(dict(
            email='joe@gmail.com',
            password='testo'
        )),
        content_type='application/json')
    data = json.loads(response.data.decode())
    assert data['status'] == 'fail'
    assert data['message'] == 'Wrong password.'
    assert not data.get('auth_token')
    assert response.content_type == 'application/json'
    assert response.status_code == 401


def test_non_registered_user_login(client):
    """Test non registered user login"""
    response = client.post(
        '/auth/login',
        data=json.dumps(dict(
            email='joe@gmail.com',
            password='test'
        )),
        content_type='application/json')
    data = json.loads(response.data.decode())
    assert data['status'] == 'fail'
    assert data['message'] == 'User does not exist.'
    assert not data.get('auth_token')
    assert response.content_type == 'application/json'
    assert response.status_code == 401
