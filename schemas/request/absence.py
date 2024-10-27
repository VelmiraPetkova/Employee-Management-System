from marshmallow import Schema, fields, validate

from models import AbsenceType


class AbsenceRequestSchema(Schema):
    from_= fields.Date(required=True)
    to_ = fields.Date(required=True)
    days = fields.Integer(required=True)
    employee = fields.Integer(required=False)
    photo = fields.String(required=False)
    photo_extension = fields.String(required=False)
    type= fields.Str(
        required=True,
        validate=validate.OneOf([role.value for role in AbsenceType], error="Invalid type of absence")
    )
    contracts_id = fields.Integer(required=False)
