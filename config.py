import os
from pathlib import Path

# 'dialect+driver://username:password@host:port/database'
postgres_local_base = 'postgresql://postgres:postgres@localhost:5432/'
database_name = 'some_db'
base_dir = Path(__file__).parent.absolute()


class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv("SECRET_KEY", 'anydfsfsafaga')

    # SQLALCHEMY_DATABASE_URI = 'postgresql:///example'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    BCRYPT_LOG_ROUNDS = 13

    AUDIO_UPLOADS = base_dir.joinpath(
        'media/audio/uploads')
    AUDIO_EXPORTS = base_dir.joinpath(
        'media/audio/exports')
    SESSION_COOKIE_SECURE = True
    JWT_EXP = 604800


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or \
        'sqlite:///' + str(base_dir.joinpath('data.sqlite'))


class DevelopmentConfig(Config):
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 4
    # SQLALCHEMY_DATABASE_URI = postgres_local_base + database_name
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URL') or \
        'sqlite:///' + str(base_dir.joinpath('data-dev.sqlite'))
    SESSION_COOKIE_SECURE = False


class TestingConfig(Config):
    TESTING = True

    BCRYPT_LOG_ROUNDS = 4
    # SQLALCHEMY_DATABASE_URI = postgres_local_base + database_name + '_test'
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL') or \
        'sqlite://'
    PRESERVE_CONTEXT_ON_EXCEPTION = False

    SESSION_COOKIE_SECURE = False
    RQ_CONNECTION_CLASS = 'fakeredis.FakeStrictRedis'
    AUDIO_UPLOADS = base_dir.joinpath(
        'tests/audio/uploads')
    AUDIO_EXPORTS = base_dir.joinpath(
        'tests/audio/exports')
    RQ_ASYNC = False
    JWT_EXP = 5
