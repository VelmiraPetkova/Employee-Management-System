from flask import request
from flask_restful import Resource
from werkzeug.exceptions import BadRequest
from werkzeug.security import check_password_hash

from managers.auth import AuthManager
from models import UserModel
from schemas.request.users import UserRegisterRequestSchema, UserLoginRequestSchema
from schemas.response.users import UserAuthResponseSchema
from utils.decorators import validate_schema


class UserRegisterResource(Resource):
    @validate_schema(UserRegisterRequestSchema)
    def post(self):
        data = request.get_json()
        user = AuthManager.create_user(data)
        token= AuthManager.encode_token(user)
        return UserAuthResponseSchema().dump({"token": token})
        #return UserOutSchema().dump(user), 201


class UserLoginResource(Resource):
    @validate_schema(UserLoginRequestSchema)
    def post(self):
        data = request.get_json()
        user = AuthManager.login_user(data)
        token= AuthManager.encode_token(user)
        return UserAuthResponseSchema().dump({"token": token})


#api.add_resource(UserRegisterResource, '')