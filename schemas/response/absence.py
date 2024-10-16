from marshmallow import fields, Schema


class AbsenceResponse(Schema):
    id = fields.Integer(required=True)
    created_at = fields.DateTime(required=True)
    #status = fields.Enum(ContractType, by_value=True)

class AbsenceErrorResponse(Schema):
    message = fields.String()