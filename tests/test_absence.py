from models import ContractsModel, AbsenceModel, UserModel
from tests.factories import UserFactory
from tests.test_base import TestBase, generate_token


class TestAbsence(TestBase):
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


    def test_check_employee(self):
        pass



    def test_create_absence(self):
        contracts = ContractsModel.query.all()
        assert len(contracts) == 0

        absence = AbsenceModel.query.all()
        assert len(absence) == 0





