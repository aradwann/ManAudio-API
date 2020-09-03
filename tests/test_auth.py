import json
import time
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


def test_user_status(client):
    """Test user status"""
    # register user
    reg_response = client.post(
        '/auth/register',
        data=json.dumps(dict(
            email='joe@gmail.com',
            password='test'
        )),
        content_type='application/json'
    )
    # get registered user status
    response = client.get(
        '/auth/status',
        headers=dict(
            Authorization='Bearer ' + json.loads(
                reg_response.data.decode()
            )['auth_token']
        )
    )
    data = json.loads(response.data.decode())
    assert data['status'] == 'success'
    assert data['data'] is not None
    assert data['data']['email'] == 'joe@gmail.com'
    assert data['data']['admin'] is 'true' or 'false'
    assert response.status_code, 200


def test_valid_logout(client):
    """Test user logout"""

    # register user
    register_response = client.post(
        '/auth/register',
        data=json.dumps(dict(
            email='joe@gmail.com',
            password='test'
        )),
        content_type='application/json'
    )
    data = json.loads(register_response.data.decode())
    assert (data['status'] == 'success')
    assert (data['message'] == 'Successfully registered.')
    assert (data['auth_token'])
    assert (register_response.content_type == 'application/json')
    assert (register_response.status_code == 201)

    # login user
    login_response = client.post(
        '/auth/login',
        data=json.dumps(dict(
            email='joe@gmail.com',
            password='test'
        )),
        content_type='application/json')
    data = json.loads(login_response.data.decode())
    assert data['status'] == 'success'
    assert data['message'] == 'Successfully logged in.'
    assert data['auth_token']
    assert login_response.content_type == 'application/json'
    assert login_response.status_code == 200

    # logout user

    response = client.post(
        '/auth/logout',
        headers=dict(
            Authorization='Bearer ' + json.loads(
                login_response.data.decode()
            )['auth_token']
        )
    )
    data = json.loads(response.data.decode())
    assert data['status'] == 'success'
    assert data['message'] == 'Successfully logged out.'
    assert response.status_code == 200


def test_invalid_logout(client):
    """Test user logout"""

    # register user
    register_response = client.post(
        '/auth/register',
        data=json.dumps(dict(
            email='joe@gmail.com',
            password='test'
        )),
        content_type='application/json'
    )
    data = json.loads(register_response.data.decode())
    assert (data['status'] == 'success')
    assert (data['message'] == 'Successfully registered.')
    assert (data['auth_token'])
    assert (register_response.content_type == 'application/json')
    assert (register_response.status_code == 201)

    # login user
    login_response = client.post(
        '/auth/login',
        data=json.dumps(dict(
            email='joe@gmail.com',
            password='test'
        )),
        content_type='application/json')
    data = json.loads(login_response.data.decode())
    assert data['status'] == 'success'
    assert data['message'] == 'Successfully logged in.'
    assert data['auth_token']
    assert login_response.content_type == 'application/json'
    assert login_response.status_code == 200

    # sleep 6 secs to make the token expire 'its lifetime is 5 secs'
    time.sleep(6)

    # logout user with invalid token

    response = client.post(
        '/auth/logout',
        headers=dict(
            Authorization='Bearer ' + json.loads(
                login_response.data.decode()
            )['auth_token']
        )
    )
    data = json.loads(response.data.decode())
    assert data['status'] == 'fail'
    assert data['message'] == 'Signature expired, Please login again.'
    assert response.status_code == 401
