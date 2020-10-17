from . import auth
from flask import jsonify


class AuthError(Exception):
    '''
    AuthError Exception
    A standardized way to communicate auth failure modes
    '''

    def __init__(self, message, status_code):
        self.message = message
        self.status_code = status_code


class InternalServerError(AuthError):
    pass


@auth.app_errorhandler(InternalServerError)
@auth.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        'success': False,
        'message': error.message
    }), error.status_code


@auth.app_errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "message": "not_found"
    }), 404


@auth.app_errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        "success": False,
        "message": "method not allowed"
    }), 405


@auth.app_errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "message": "unprocessable"
    }), 422
