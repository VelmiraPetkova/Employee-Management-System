import os
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

import pytest

from db import db
from managers.absence import AbsenceManager
from managers.contract import ContractChangeManager
from models import ContractsModel, AbsenceModel, UserModel, UserType, State, ContractType
from services.s3 import S3Service
from tests.factories import UserFactory, ContractFactory, AbsenceFactory
from tests.help import photo
from tests.test_base import TestBase, generate_token


class TestAbsence(TestBase):
    @patch.object(S3Service,'upload_file', return_value="some_url_.com" )
    def test_create_absence(self, mock_s3_upload):
        absence = AbsenceModel.query.all()
        assert len(absence) == 0

        user = UserFactory()
        token = generate_token(user)
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        from_date = (datetime.now() + timedelta(days=4)).strftime('%Y-%m-%d')
        to_date = (datetime.now() + timedelta(days=6)).strftime('%Y-%m-%d')

        contract = ContractFactory()

        data = {"from_": from_date,
                "to_": to_date,
                "days": "2",
                "employee": user.id,
                "type": "sick",
                "photo": photo,
                "photo_extension": "jpeg"
        }

        res = self.client.post("/absenceregister", json=data, headers=headers)
        absence = AbsenceModel.query.all()
        assert len(absence) == 1
        assert res.status_code == 201
        assert res.json['photo'] == 'some_url_.com'



    def test_required_fields_missing_raises(self):
        user = UserFactory()
        token = generate_token(user)
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        data = {}
        res = self.client.post("/absenceregister", json=data, headers=headers)
        assert res.status_code == 400
        assert res.json == {'message': {'days': ['Missing data for required field.'],
                                        'from_': ['Missing data for required field.'],
                                        'to_': ['Missing data for required field.'],
                                        'type': ['Missing data for required field.']}}


    def test_contract_start_date_and_absence_date(self):
        user = UserFactory()
        contract = ContractFactory()

        token = generate_token(user)
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        from_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        to_date = (datetime.now() + timedelta(days=5)).strftime('%Y-%m-%d')
        data = {"from_": from_date,
                "to_": to_date,
                "days": "2",
                "employee": user.id,
                "type": "sick"
        }
        res = self.client.post("/absenceregister", json=data, headers=headers)
        assert res.status_code == 400
        assert res.json == {'message': 'The absence dates are not within the active contract period.'}



    def test_contract_civil(self):
        user = UserFactory()
        contract = ContractFactory(contract_type= ContractType.civil, employee=user.id)

        token = generate_token(user)
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        from_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        to_date = (datetime.now() + timedelta(days=5)).strftime('%Y-%m-%d')
        data = {"from_": from_date,
                "to_": to_date,
                "days": "2",
                "employee": user.id,
                "type": "sick"
        }
        res = self.client.post("/absenceregister", json=data, headers=headers)
        assert res.status_code == 400
        assert res.json == {'message': 'Your contract is not eligible for absence'}


    def test_approve_absence_success(self):
        absence = AbsenceModel.query.all()
        assert len(absence) == 0
        user = UserFactory(role=UserType.manager)

        contract = ContractFactory(employee=user.id)
        absence = AbsenceFactory(from_ = contract.effective,
                                 employee = user.id,
                                 contracts_id = contract.id)
        absence = AbsenceModel.query.all()
        assert len(absence) == 1
        assert absence[0].status == State.pending

        #user_approve = UserFactory(role=UserType.manager)

        token = generate_token(user)
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        url= f"/absences/{absence[0].id}/approve"
        res = self.client.get(url, headers=headers)
        #TODO It should return a 204 code
        assert res.status_code == 200


    def test_reject_absence_success(self):
        absence = AbsenceModel.query.all()
        assert len(absence) == 0
        user = UserFactory(role=UserType.manager)

        contract = ContractFactory(employee=user.id)
        absence = AbsenceFactory(from_ = contract.effective,
                                 employee = user.id,
                                 contracts_id = contract.id)
        absence = AbsenceModel.query.all()
        assert len(absence) == 1
        assert absence[0].status == State.pending

        #user_approve = UserFactory(role=UserType.manager)

        token = generate_token(user)
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        url= f"/absences/{absence[0].id}/reject"
        res = self.client.get(url, headers=headers)
        #TODO It should return a 204 code
        assert res.status_code == 200


    def test_delete_absence_success(self):
        user = UserFactory()
        contract = ContractFactory(employee=user.id)
        absence = AbsenceFactory(employee=user.id,contracts_id=contract.id)

        absence = AbsenceModel.query.all()
        assert len(absence) == 1

        token = generate_token(user)
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        url = f"/absences/{absence[0].id}/delete"
        res = self.client.delete(url, headers=headers)

        absence = AbsenceModel.query.all()
        assert len(absence) == 0










