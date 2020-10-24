from flask import request
from .errors import AuthError
from ..models import User
from functools import wraps


def get_token_auth_header():
    """get auth token from request headers
    raise AuthError if something is wrong if not
    return the token
    """
    auth_header = request.headers.get('Authorization', None)
    if not auth_header:
        raise AuthError(
            status_code=401,
            message='Authorization header is expected.'
        )

    auth_parts = auth_header.split()
    if auth_parts[0].lower() != 'bearer':
        raise AuthError(
            status_code=401,
            message='Authorization header must start with "Bearer".'
        )
    elif len(auth_parts) == 1:
        raise AuthError(
            status_code=401,
            message='Token not found.'
        )
    elif len(auth_parts) > 2:
        raise AuthError(
            status_code=401,
            message='Token not found.'
        )
    token = auth_parts[1]
    return token


def auth_required(func):
    """
    require the request sender to have a valid JWT
    Passes the payload to the wrapped function
    Payload here is the user's id
    """
    @wraps(func)
    def wrapper_auth_required(*args, **kwargs):
        token = get_token_auth_header()
        resp = User.decode_auth_token(token)
        if isinstance(resp, str):
            raise AuthError(
                status_code=401,
                message=resp
            )
        return func(resp, *args, **kwargs)
    return wrapper_auth_required
