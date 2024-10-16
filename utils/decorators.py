from flask import request
from marshmallow import validates_schema
from sqlalchemy.sql.functions import current_user
from werkzeug.exceptions import BadRequest, Forbidden
from flask_httpauth import HTTPTokenAuth

from managers.auth import auth
from models import UserModel


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


def permission_required(permission):
    def decorator(func):
        def wrapper(*args, **kwargs):
            current_user  = auth.current_user()
            if current_user.role == permission:
                return func(*args, **kwargs)
            raise Forbidden("You don't have permission to perform this action.")
        return wrapper
    return decorator
