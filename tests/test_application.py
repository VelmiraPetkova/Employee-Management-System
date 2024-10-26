from email._header_value_parser import ContentType

from managers.contract import ManagerContract
from models import UserType, ContractType, ContractsModel
from tests.factories import UserFactory
from tests.test_base import TestBase, generate_token


class TestLoginAndAuthorizationRequired(TestBase):
    def test_auth_is_required(self):
        all_urls = [
            ('GET', '/contract'),
            ('POST', '/contract'),
            ('POST', '/absenceregister'),
            ('PUT','/addmanager/user/1'),
            ('GET', '/absences/1/approve'),
            ('GET','/absences/1/reject'),
            ('PUT', '/change/1/contract'),
            ('DELETE','/absences/1/delete'),
        ]

        for method, url in all_urls:
            if method == 'GET':
                res = self.client.get(url)
            elif method == 'POST':
                res = self.client.post(url)
            elif method == 'PUT':
                res = self.client.put(url)
            elif method == 'DELETE':
                res = self.client.delete(url)

            assert res.status_code == 401
            assert res.json['message'] == 'Invalid token or missing token'




    def test_permission_required_create_or_change_contract(self):
        user = UserFactory()
        token = generate_token(user)
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        res = self.client.post('/contract', headers=headers)
        assert res.status_code == 403
        assert res.json['message'] == "You don't have permission to perform this action."

        res = self.client.put('/change/1/contract', headers=headers)
        assert res.status_code == 403
        assert res.json['message'] == "You don't have permission to perform this action."


    def test_permission_required_approve_reject_absence(self):
        user = UserFactory()
        token = generate_token(user)
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        res = self.client.get('/absences/1/approve', headers=headers)
        assert res.status_code == 403
        assert res.json['message'] == "You don't have permission to perform this action."

        res = self.client.get('/absences/1/reject', headers=headers)
        assert res.status_code == 403
        assert res.json['message'] == "You don't have permission to perform this action."