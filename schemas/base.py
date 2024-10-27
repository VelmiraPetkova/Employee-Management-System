from datetime import datetime, date

from marshmallow import Schema, fields,validate

from models import ContractType
from utils.custom_validators import *


class UserRequestBase(Schema):
    email = fields.String(required=True,
                          validate=validate.And(email_is_valid))
    password = fields.String(required=True,
                             validate=validate.And(validate.Length(min=8, max=200), validate_password))



class ContractBase(Schema):
    employee = fields.Integer(required=True)
    effective = fields.Date(required=True)
    end_date = fields.Date(required=False)
    salary = fields.Float(required=True, validate=lambda x: x > 0)
    hours = fields.Float(
        validate=[validate.Range(min=0, max=8, error="Hours must be between 0 and 8."), validate_work_hours]
    )
    department = fields.String(required=True)
    position = fields.String(required=True)
    contract_type = fields.Str(
        required=False,
        validate=validate.OneOf([role.value for role in ContractType], error="Invalid type of contract")
    )
