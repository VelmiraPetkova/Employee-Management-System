from flask import request
from marshmallow import validates_schema
from werkzeug.exceptions import BadRequest
from flask_httpauth import HTTPTokenAuth

from models import UserModel

auth = HTTPTokenAuth(scheme='Bearer')



def validate_schema(schema_name):
    def decorator(func):
        def wrapper(*args, **kwargs):
            schema = schema_name()
            data = request.get_json()
            errors = schema.validate(data)
            if not errors:
                return func(*args, **kwargs)
            raise BadRequest(errors)
        return wrapper
    return decorator


