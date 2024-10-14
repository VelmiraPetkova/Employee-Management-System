from marshmallow import Schema, fields,validate

from utils.custom_validators import *


class UserRequestBase(Schema):
    email = fields.String(required=True,
                          validate=validate.And(email_is_valid))
    password = fields.String(required=True,
                             validate=validate.And(validate.Length(min=8, max=200), validate_password))