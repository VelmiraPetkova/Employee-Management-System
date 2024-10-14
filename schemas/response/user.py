from marshmallow import Schema, fields

class UserOutSchema(Schema):
    id = fields.Integer()
    created_on = fields.DateTime()
    updated_on = fields.DateTime()
