from flask import request
from .errors import AuthError


def get_token_auth_header():
    """get auth token from request headers
    raise AuthError if something is wrong if not
    return the token
    """
    auth_header = request.headers.get('Authorization', None)
    if not auth_header:
        raise AuthError({
            'status': 'fail',
            'message': 'Authorization header is expected.'
        }, 401)

    auth_parts = auth_header.split()
    if auth_parts[0].lower() != 'bearer':
        raise AuthError({
            'status': 'fail',
            'message': 'Authorization header must start with "Bearer".'
        }, 401)
    elif len(auth_parts) == 1:
        raise AuthError({
            'status': 'fail',
            'message': 'Token not found.'
        }, 401)
    elif len(auth_parts) > 2:
        raise AuthError({
            'status': 'fail',
            'message': 'Token not found.'
        }, 401)
    token = auth_parts[1]
    return token
