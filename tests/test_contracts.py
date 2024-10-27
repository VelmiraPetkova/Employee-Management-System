from datetime import datetime, timedelta

from models import UserType, ContractsModel, AbsenceModel
from tests.factories import UserFactory
from tests.test_base import TestBase, generate_token


class TestContract(TestBase):
    def test_required_fields_missing_raises(self):
        user = UserFactory(role = UserType.accountant)
        token = generate_token(user)
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }


        data = {}
        res = self.client.post("/contract", json=data, headers=headers)
        assert res.status_code == 400
        assert res.json == {'message': {'department': ['Missing data for required field.'],
                                        'effective': ['Missing data for required field.'],
                                        'employee': ['Missing data for required field.'],
                                        'position': ['Missing data for required field.'],
                                        'salary': ['Missing data for required field.']}}



    """Test that a temporary contract without an end date raises an error."""
    def test_temporary_contract_missing_end_date(self):
        user = UserFactory(role=UserType.accountant)
        token = generate_token(user)
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }


        data={"employee": 1,
              "effective": "2024-10-20",
              "salary": 1000,
              "hours": 8,
              "department": "IT",
              "position": "Developer",
              "contract_type": "temporary",
              }

        res = self.client.post("/contract", json=data, headers=headers)
        assert res.status_code == 400
        assert res.json == {'message': 'End date cannot be empty when contract is temporary'}


    def test_temporary_contract_with_error_end_date(self):
        user = UserFactory(role=UserType.accountant)
        token = generate_token(user)
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        data={"employee": 1,
              "effective": "2024-10-20",
              "salary": 1000,
              "hours": 8,
              "department": "IT",
              "position": "Developer",
              "contract_type": "temporary",
              "end_date": "2023-12-31"
              }

        res = self.client.post("/contract", json=data, headers=headers)
        assert res.status_code == 400
        assert res.json == {'message': 'The end date cannot be less than the start date'}

    """Test that a permanent contract with an end date raises an error."""
    def test_permanent_contract_with_end_date(self):
        user = UserFactory(role=UserType.accountant)
        token = generate_token(user)
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        data = {"employee": 1,
                "effective": "2024-10-20",
                "salary": 1000,
                "hours": 8,
                "department": "IT",
                "position": "Developer",
                "contract_type": "permanent",
                "end_date": "2023-12-31"
                }

        res = self.client.post("/contract", json=data, headers=headers)
        assert res.status_code == 400
        assert res.json == {'message': 'If you have a contract end date, change its type'}

    def test_existing_employee(self):
        user = UserFactory(role=UserType.accountant)
        token = generate_token(user)
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        data = {"employee": "1000000000000",
                "effective": "2024-10-20",
                "salary": 1000,
                "hours": 8,
                "department": "IT",
                "position": "Developer",
                "contract_type": "permanent",
                "end_date": "2023-12-31"
                }

        res = self.client.post("/contract", json=data, headers=headers)
        assert res.status_code == 400
        assert res.json == {'message': 'If you have a contract end date, change its type'}

    def test_create_contract(self):
        contracts = ContractsModel.query.all()
        assert len(contracts) == 0

        absence = AbsenceModel.query.all()
        assert len(absence) == 0

        user = UserFactory(role=UserType.accountant)
        token = generate_token(user)
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        effective_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')

        data = {"employee": user.id,
                "effective": effective_date,
                "salary": 9000,
                "hours": 7,
                "department": "IT",
                "position": "Developer"
        }
        res = self.client.post("/contract", json=data, headers=headers)
        assert res.status_code == 201

















