from datetime import datetime, timedelta
from unittest.mock import patch

import pytest

from managers.absence import AbsenceManager
from models import UserType, ContractsModel, AbsenceModel
from services.SES import SEService
from tests.factories import UserFactory, ContractFactory
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

    @patch.object(SEService, 'send_email')
    @patch.object(SEService, 'create_client')
    def test_create_contract(self,mock_create_client,mock_send_email):
        contracts = ContractsModel.query.all()
        assert len(contracts) == 0

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
        mock_create_client.assert_called_once()
        mock_send_email.assert_called_once_with(user.name, user.email)


#    def test_take_contract_with_existing_employee(self):
#        user = UserFactory(role=UserType.accountant)
#        employee = user.id
#        contract = ContractFactory(employee=employee)
#
#      # Act: Attempt to retrieve contract by employee ID
#        result = ContractsModel.query.filter_by(employee=employee).first()
#
#       # Assert: Verify that the contract is returned
#        assert result.id == contract.id
#        assert result.employee == employee


    def test_take_contract_with_nonexistent_employee(self):
        # Act and Assert: Attempt to retrieve contract with an invalid employee ID
        non_existent_employee_id = 999
        with pytest.raises(Exception) as exc_info:
             AbsenceManager.take_contract(employee=non_existent_employee_id)
        assert f"No contract found for employee with ID {non_existent_employee_id}" in str(exc_info.value)