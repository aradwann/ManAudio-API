from . import auth
from app import db, bcrypt
from flask import request, make_response, jsonify
from app.models import User, BlackListToken


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
                'status': 'success',
                'message': 'Successfully registered.',
                'auth_token': auth_token.decode()
            }
            return make_response(jsonify(response_object)), 201
        except Exception as e:
            print(e)
            response_object = {
                'status': 'fail',
                'message': 'Some error occurred. Please try again.'
            }
            return make_response(jsonify(response_object)), 401
    else:
        response_object = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }
        return make_response(jsonify(response_object)), 202


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
                response_object = {
                    'status': 'fail',
                    'message': 'Wrong password.'
                }
                return make_response(jsonify(response_object)), 401
        else:
            response_object = {
                'status': 'fail',
                'message': 'User does not exist.'
            }
            return make_response(jsonify(response_object)), 401

    except Exception as e:
        print(e)
        response_object = {
            'status': 'fail',
            'message': 'Try again',
        }
        return make_response(jsonify(response_object)), 500


@auth.route('/status', methods=['GET'])
def status():
    # get the auth token
    auth_header = request.headers.get('Authorization')
    if auth_header:
        try:
            auth_token = auth_header.split(" ")[1]
        except IndexError:
            response_object = {
                'status': 'fail',
                'message': 'Bearer token malformed.'
            }
            return make_response(jsonify(response_object)), 401
    else:
        auth_token = ''
    if auth_token:
        resp = User.decode_auth_token(auth_token)
        if not isinstance(resp, str):
            user = User.query.filter_by(id=resp).first()
            response_object = {
                'status': 'success',
                'data': {
                    'user_id': user.id,
                    'email': user.email,
                    'admin': user.admin,
                    'registered_on': user.registered_on
                }
            }
            return make_response(jsonify(response_object)), 200
        response_object = {
            'status': 'fail',
            'message': resp
        }
        return make_response(jsonify(response_object)), 401
    else:
        response_object = {
            'status': 'fail',
            'message': 'Provide a valid auth token.'
        }
        return make_response(jsonify(response_object)), 401


@auth.route('/logout', methods=['POST'])
def logout():
    # get the auth token
    auth_header = request.headers.get('Authorization')
    if auth_header:
        try:
            auth_token = auth_header.split(" ")[1]
        except IndexError:
            response_object = {
                'status': 'fail',
                'message': 'Bearer token malformed.'
            }
            return make_response(jsonify(response_object)), 401

        if auth_token:
            response = User.decode_auth_token(auth_token)
            if not isinstance(response, str):
                # mark token as blacklisted
                blacklist_token = BlackListToken(token=auth_token)
                try:
                    # insert token
                    db.session.add(blacklist_token)
                    db.session.commit()
                    response_object = {
                        'status': 'success',
                        'message': 'Successfully logged out.'
                    }
                    return make_response(jsonify(response_object)), 200
                except Exception as e:
                    print(e)
                    response_object = {
                        'status': 'fail',
                        'message': e
                    }
                    return make_response(jsonify(response_object)), 200
            else:
                response_object = {
                    'status': 'fail',
                    'message': response
                }
                return make_response(jsonify(response_object)), 401
        else:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return make_response(jsonify(response_object)), 403
