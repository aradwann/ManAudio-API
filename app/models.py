import datetime
import jwt
from flask import current_app
from app import db, bcrypt


class User(db.Model):
    """User model for storing user related details"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, email, password, admin=False):
        """User constructor

        Args:
            email (string): user email
            password (string): user password
            admin (bool, optional): is user adim. Defaults to False.
        """
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password, current_app.config['BCRYPT_LOG_ROUNDS']).decode()
        self.registered_on = datetime.datetime.now()
        self.admin = admin

    def encode_auth_token(self, user_id):
        """ Generates Auth Token and returns it

        Args:
            user_id (int): user id
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(
                    days=0, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                current_app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """Decodes the auth token
            returns payload[sub] == user id
        Args:
            auth_token (jwt): JWT
        """
        try:
            payload = jwt.decode(auth_token, current_app.config.get(
                'SECRET_KEY'), algorithms='HS256')
            return payload['sub']

        except jwt.ExpiredSignatureError:
            return 'Signature expired, Please login again.'
        except jwt.InvalidTokenError:
            return 'Invalid Token, Please login.'


class BlackListToken(db.Model):
    """
    Token model for storing blacklisted and logout tokens
    """
    __tablename__ = 'blacklist_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.now()

    def __repr__(self):
        return f'<id: {self.id} token: {self.token}'
