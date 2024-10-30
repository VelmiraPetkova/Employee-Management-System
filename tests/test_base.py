from unittest.mock import MagicMock

import pytest
from flask_testing import TestCase
from werkzeug.security import generate_password_hash

from config import create_app
from db import db
from managers.auth import AuthManager
from models import UserModel, UserType, State


def generate_token(user):
    return AuthManager.encode_token(user)


@pytest.fixture
def absence():
    return MagicMock(id=1, employee=1, status=State.pending)

class TestBase(TestCase):
    def create_app(self):
        return create_app('config.TestingConfig')

# before run  test method, create db for test
    def setUp(self):
        db.init_app(self.app)
        db.create_all()
        db.session.commit()

    # after finish test method, drop db for test
    def tearDown(self):
        db.session.rollback()  # Rollback any uncommitted transaction
        db.session.remove()
        db.drop_all()




