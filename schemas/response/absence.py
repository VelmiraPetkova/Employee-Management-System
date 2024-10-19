from marshmallow import fields, Schema

from models import ContractType


class AbsenceResponse(Schema):
    id = fields.Integer(required=True)
    created_at = fields.DateTime(required=True)
    photo=fields.String(required=False)
    status = fields.Enum(ContractType, by_value=True)

class AbsenceErrorResponse(Schema):
    message = fields.String()