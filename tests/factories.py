from datetime import UTC, datetime, timedelta
import random

import factory


from db import db
from models import UserModel, UserType, ContractsModel, ContractType, AbsenceModel, AbsenceType, State


class BaseFactory(factory.Factory):
    @classmethod
    def create(cls, **kwargs):
        object = super().create(**kwargs)
        db.session.add(object)
        db.session.commit()
        return object


class UserFactory(BaseFactory):
    class Meta:
        model = UserModel

    id = factory.Sequence(lambda n: n)
    name = factory.Faker('name')
    civil_number = factory.Faker('bothify', text='##########')
    phone = factory.Faker('bothify', text='08########')
    iban = factory.Faker('iban')
    email = factory.Faker('email')
    role = UserType.employee
    password = factory.Faker('password')
    created_on = factory.Faker("date_time", tzinfo=UTC)


def get_user_id():
    return UserFactory.id

departments = ["IT", "HR", "Sales", "Finance", "Marketing"]
positions = ["Developer", "Manager", "Analyst", "Consultant", "Designer"]

class ContractFactory(BaseFactory):
    class Meta:
        model = ContractsModel


    id = factory.Sequence(lambda n: n)
    employee = UserFactory.id
    effective = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    salary = 5000.0
    hours = 8.0,
    department = random.choice(departments)
    position = random.choice(positions)
    created_on = datetime.now()
    updated_on = datetime.now()
    user_id = UserFactory.id
    contract_type= ContractType.permanent


class AbsenceFactory(BaseFactory):
    class Meta:
        model = AbsenceModel

    id = factory.Sequence(lambda n: n)
    from_ = datetime.now()
    to_ = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    days = 2
    type = AbsenceType.sick
    employee = factory.LazyFunction(get_user_id)
    contracts_id = ContractFactory.id
    status= State.pending.name





