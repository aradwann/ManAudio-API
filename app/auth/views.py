from . import auth
from app import db, bcrypt
from flask import request, make_response, jsonify
from app.models import User


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
            responseObject = {
                'status': 'success',
                'message': 'Successfully registered.',
                'auth_token': auth_token.decode()
            }
            return make_response(jsonify(responseObject)), 201
        except Exception as e:
            print(e)
            responseObject = {
                'status': 'fail',
                'message': 'Some error occurred. Please try again.'
            }
            return make_response(jsonify(responseObject)), 401
    else:
        responseObject = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }
        return make_response(jsonify(responseObject)), 202


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
                        'status': 'success',
                        'message': 'Successfully logged in.',
                        'auth_token': auth_token.decode()
                    }
                    return make_response(jsonify(response_object)), 200
            else:
                responseObject = {
                    'status': 'fail',
                    'message': 'Wrong password.'
                }
                return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'User does not exist.'
            }
            return make_response(jsonify(responseObject)), 401

    except Exception as e:
        print(e)
        response_object = {
            'status': 'fail',
            'message': 'Try again',
        }
        return make_response(jsonify(response_object)), 500
