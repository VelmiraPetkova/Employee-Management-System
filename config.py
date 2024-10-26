from decouple import config
from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api

from db import db
from resources.routes import routes


#from decouple import config


class DevelopmentConfig:
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = (f'postgresql://'
    f'{config('DB_USER')}:'
    f'{config('DB_PASSWORD')}@localhost:'
    f'{config('DB_PORT')}/{config('DB_NAME')}')


class TestingConfig:
    """Configurations for Testing, with a separate test database."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = (f'postgresql://'
    f'{config('DB_USER')}:'
    f'{config('DB_PASSWORD')}@localhost:'
    f'{config('DB_PORT')}/{config('TEST_DB_NAME')}')
    DEBUG = True


def create_app(config = 'config.DevelopmentConfig'):
    app = Flask(__name__)
    app.config.from_object(config)

    api = Api(app)
    migrate = Migrate(app, db)


    [api.add_resource(*route) for route in routes]
    return app


