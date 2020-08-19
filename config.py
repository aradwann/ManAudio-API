import os
from pathlib import Path

postgres_local_base = 'postgresql://postgres:@localhost/'
database_name = 'flask_jwt_auth'

class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get("SECRET_KEY", 'anydfsfsafaga')
    SQLALCHEMY_DATABASE_URI = 'postgresql:///example'

    DB_NAME = "production-db"
    DB_USERNAME = "admin"
    DB_PASSWORD = "example"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    BCRYPT_LOG_ROUNDS = 13

    AUDIO_UPLOADS = Path(__file__).parent.absolute().joinpath(
        'media/audio/uploads')
    AUDIO_EXPORTS = Path(__file__).parent.absolute().joinpath(
        'media/audio/exports')
    SESSION_COOKIE_SECURE = True


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True

    DB_NAME = "development-db"
    DB_USERNAME = "admin"
    DB_PASSWORD = "example"
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = postgres_local_base + database_name

    SESSION_COOKIE_SECURE = False


class TestingConfig(Config):
    TESTING = True

    DB_NAME = "development-db"
    DB_USERNAME = "admin"
    DB_PASSWORD = "example"
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = postgres_local_base + database_name + '_test'
    PRESERVE_CONTEXT_ON_EXCEPTION = False

    SESSION_COOKIE_SECURE = False
