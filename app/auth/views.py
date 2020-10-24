from . import auth
from app import db, bcrypt
from flask import request, make_response, jsonify
from app.models import User, BlacklistToken
from .decorators import auth_required
from .errors import AuthError, InternalServerError


@auth.route('/register', methods=['POST'])
def register():
    """ A view function for the route '/register' to
    register new users
    """
    # get the post data
    post_data = request.get_json()
    # check if user already exists
    user = User.query.filter_by(email=post_data.get('email')).first()
    if not user:
        try:
            user = User(
                email=post_data.get('email'),
                password=post_data.get('password')
            )

            # insert the user
            db.session.add(user)
            db.session.commit()
            # generate the auth token
            auth_token = user.encode_auth_token(user.id)
            response_object = {
                'success': True,
                'message': 'Successfully registered.',
                'auth_token': auth_token.decode()
            }
            return make_response(jsonify(response_object)), 201
        except AuthError:
            raise AuthError(
                status_code=401,
                message='Some error occurred. Please try again.'
            )
    else:
        raise AuthError(
            status_code=202,
            message='User already exists. Please Log in.',
        )


@auth.route('/login', methods=['POST'])
def login():
    """ A view function for the route '/login'
    for registered users to login
    """
    post_data = request.get_json()

    try:
        # fetch the user data
        user = User.query.filter_by(email=post_data.get('email')).first()
        if user:
            if bcrypt.check_password_hash(
                    user.password, post_data.get('password')):

                auth_token = user.encode_auth_token(user.id)
                if auth_token:
                    response_object = {
                        'success': True,
                        'message': 'Successfully logged in.',
                        'auth_token': auth_token.decode()
                    }
                    return make_response(jsonify(response_object)), 200
            else:
                raise AuthError(
                    status_code=401,
                    message='Wrong password.'
                )
        else:
            raise AuthError(
                status_code=401,
                message='User does not exist.'
            )
    except InternalServerError:
        raise InternalServerError(
            status_code=500,
            message='there is an error! Try again',
        )


@auth.route('/status', methods=['GET'])
@auth_required
def status(payload):
    """get the user details of the currently logged in user
    Returns:
        response: user details
    """

    user = User.query.filter_by(id=payload).first()
    response_object = {
        'success': True,
        'data': {
            'user_id': user.id,
            'email': user.email,
            'admin': user.admin,
            'registered_on': user.registered_on
        }
    }
    return make_response(jsonify(response_object)), 200


@auth.route('/logout', methods=['POST'])
@auth_required
def logout(payload):
    """logout user and blacklist the loggedout user's token
        Returns:
            response: success or failure message
    """
    # mark token as blacklisted
    blacklist_token = BlacklistToken(token=payload)
    try:
        # insert token
        db.session.add(blacklist_token)
        db.session.commit()
        response_object = {
            'success': True,
            'message': 'Successfully logged out.'
        }
        return make_response(jsonify(response_object)), 200
    except Exception as e:
        print(e)
        raise AuthError(
            status_code=401,
            message=e
        )


@auth.route('/headers')
@auth_required
def headers(payload):
    print(payload)
    response_object = {
        'success': True,
        'message': 'Access Granted'
    }
    return make_response(jsonify(response_object)), 200
