from datetime import date

from marshmallow import fields, validate

from models import ContractType
from schemas.base import ContractBase
from utils.custom_validators import validate_work_hours


class RequestContractSchema(ContractBase):
    pass


class ChangeContractSchema(ContractBase):
    employee = fields.Integer(required=True)
    effective = fields.Date(required=False)
    hours = fields.Float(required=False,
        validate=[validate.Range(min=0, max=8, error="Hours must be between 0 and 8."), validate_work_hours, ]
    )
    department = fields.String(required=False)
    position = fields.String(required=False)


