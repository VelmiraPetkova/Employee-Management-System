from marshmallow import fields, Schema

from schemas.base import ContractBase


class ContractResponse(ContractBase):
    id = fields.Integer(required=True)
    created_at = fields.DateTime(required=True)
    updated_on= fields.DateTime(required=True)
    #status = fields.Enum(ContractType, by_value=True)

class ContractErrorResponse(Schema):
    message = fields.String()
