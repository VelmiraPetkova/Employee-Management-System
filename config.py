from decouple import config

class DevelopmentConfig:
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = (f'postgresql://'
    f'{config('DB_USER')}:'
    f'{config('DB_PASSWORD')}@localhost:'
    f'{config('DB_PORT')}/{config('DB_NAME')}')