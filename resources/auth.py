

from flask import request
from flask_restful import Resource

from db import db
from managers.auth import AuthManager, auth
from managers.user import UserManager
from models import UserType, UserModel
from schemas.request.users import UserRegisterRequestSchema, UserLoginRequestSchema, UserManagerSchema
from schemas.response.user import UserOutSchema
from schemas.response.users import UserAuthResponseSchema
from utils.decorators import validate_schema, permission_required


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


class AddManagerResource(Resource):
    @auth.login_required
    @permission_required([UserType.accountant])
    @validate_schema(UserManagerSchema)
    def put(self,user_id):
        data = request.get_json()
        user= UserManager.assign_manager(data,user_id)
        return UserOutSchema().dump(user)


class UserChangeResource(Resource):
        pass

class ChangePasswordResource(Resource):
    pass