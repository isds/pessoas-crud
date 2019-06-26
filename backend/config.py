# import backend.settings as settings

import settings
from datetime import timedelta


class Config:
    SECRET_KEY = settings.SECRET_KEY
    APP_PORT = int(settings.APP_PORT)
    DEBUG = settings.DEBUG
    SQLALCHEMY_DATABASE_URI = settings.DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    ENV = 'development'
    DEBUG = True


class TestingConfig(Config):
    ENV = 'testing'
    TESTING = True


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
