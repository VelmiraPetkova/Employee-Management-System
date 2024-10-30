import pytest
from werkzeug.exceptions import BadRequest

from managers.user import UserManager
from models import UserModel, UserType
from tests.factories import UserFactory
from tests.test_base import TestBase, generate_token


class TestUserManager(TestBase):
    def test_verify_user_success(self):
        user = UserFactory()
        result = UserManager._verify_user(user.id)
        assert result == user


    def test_check_manager_success(self):
        #user = UserFactory(id=1)
        user_manager = UserFactory(id=2)
        result =  UserModel.query.filter_by(id=user_manager.id).first()
        assert result ==user_manager

    def test_assign_manager_success(self):
        user=UserFactory(id=7)
        user_manager = UserFactory(id=55)
        user_request = UserFactory(role = UserType.accountant)

        token = generate_token(user_request)
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        data = {"manager": user_manager.id}
        res = self.client.put(f"/addmanager/user/{user.id}", json=data, headers=headers)
        assert res.status_code == 200



    def test_assign_manager_failure(self):
        user=UserFactory(id=10)
        user_manager = UserFactory(id=99)
        user_request = UserFactory(role = UserType.accountant)

        token = generate_token(user_request)
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        data = {"manager": "11"}

        res = self.client.put(f"/addmanager/user/{user.id}", json=data, headers=headers)
        assert res.status_code == 400
        assert res.json=={'message': 'No such manager exists'}

    def test_create_user_success(self):
        user = UserModel.query.all()
        assert len(user) == 0

        headers = {
            "Content-Type": "application/json"
        }

        data= {
                "name": "Test Test",
                "civil_number": "9408303257",
                "phone": "0811111111",
                "iban": "BG70BNBG47622021445672",
                "email": "velmira@gmail.com",
                "password": "Welmira2023-"
        }
        res = self.client.post("/register", json=data, headers=headers)
        user = UserModel.query.all()
        assert len(user) == 1


    def test_create_user_failure(self):
        user = UserModel.query.all()
        assert len(user) == 0

        headers = {
            "Content-Type": "application/json"
        }

        data= {
                "name": "Test Test",
                "civil_number": "1",
                "phone": "0811111111",
                "iban": "BG70BNBG476220445672",
                "email": "velmira@gmail..com",
                "password": "aa2023-"
        }
        res = self.client.post("/register", json=data, headers=headers)

        assert res.status_code == 400
        assert res.json=={'message': {'civil_number': ['Not a valid civil or national ID number'],
                                    'email': ['Domain must be one of the following: .com, .bg, .org, '
                                    '.net'],
                                    'password': ['Length must be between 8 and 200.',
                                        'Not a valid password']}}















