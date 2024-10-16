from marshmallow import  fields, validate

from models import UserType
from schemas.base import UserRequestBase
from utils.custom_validators import *


class UserRegisterRequestSchema(UserRequestBase):
    name = fields.String(required=True,
                         validate=validate.And(validate.Length(min=8, max=255), validate_name))
    civil_number = fields.String(required=True,
                         validate=validate.And(validate.Length(max=10), validate_phone))
    phone = fields.String(required=True,
                         validate=validate.And(validate.Length(max=10), validate_civil_number))

    iban = fields.String(required=True,
                         validate=validate.And(validate.Length(max=22), validate_iban))
    emergency_contact = fields.String(required=False, validate=validate.Length(max=50))
    date_birth = fields.String(required=False, validate=validate.Length(max=10))
    manager = fields.Integer(required=False)
    role = fields.Str(
        required=False,
        validate=validate.OneOf([role.value for role in UserType], error="Invalid type of role")
    )


class UserLoginRequestSchema(UserRequestBase):
    pass