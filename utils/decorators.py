from flask import request
from werkzeug.exceptions import BadRequest, Forbidden
from flask_httpauth import HTTPTokenAuth

from managers.auth import auth
from models import UserModel, UserType


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


def permission_required(required_roles: list[UserType]):
    def decorator(func):
        def wrapper(*args, **kwargs):
            current_user  = auth.current_user()
            if current_user.role in required_roles:
                return func(*args, **kwargs)
            raise Forbidden("You don't have permission to perform this action.")
        return wrapper
    return decorator
