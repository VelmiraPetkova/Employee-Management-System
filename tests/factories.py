from datetime import UTC
import random

import factory


from db import db
from models import UserModel, UserType, ContractsModel, ContractType


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


