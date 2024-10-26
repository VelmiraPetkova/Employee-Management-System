from flask_testing import TestCase
from werkzeug.security import generate_password_hash

from config import create_app
from db import db
from managers.auth import AuthManager
from models import UserModel, UserType


def generate_token(user):
    return AuthManager.encode_token(user)


class TestBase(TestCase):
    def create_app(self):
        return create_app('config.TestingConfig')

# before run  test method, create db for test
    def setUp(self):
        db.init_app(self.app)
        db.create_all()

# after finish test method, drop db for test
    def tearDown(self):
        db.session.remove()
        db.drop_all()



