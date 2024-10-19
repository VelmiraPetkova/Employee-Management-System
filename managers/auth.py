from datetime import datetime, timedelta, UTC

import jwt
from decouple import config
from flask_httpauth import HTTPTokenAuth
from jwt import DecodeError, InvalidSignatureError
from werkzeug.exceptions import BadRequest, Unauthorized
from werkzeug.security import generate_password_hash, check_password_hash

from db import db
from models import UserModel
from services.SES import SEService
from utils.clean_data import *


class AuthManager:
    @staticmethod
    def create_user(user_data):
        user_data["password"] = generate_password_hash(user_data["password"], method='pbkdf2:sha256')
        user_data["name"] = clean_name(user_data["name"])
        user_data["phone"] = clean_phone(user_data["phone"])
        user_data["civil_number"] = clean_civil_number(user_data["civil_number"])
        user_data["iban"] = clean_iban(user_data["iban"])
        user = UserModel(**user_data)
        db.session.add(user)
        db.session.commit()
        SEService().verify_email_identity(user.email)
        return user

    @staticmethod
    def login_user(user_data):
        # is there  exist email in base
        user= UserModel.query.filter_by(email=user_data['email']).first()
        if not user:
            raise BadRequest("Invalid email or password")

        if not check_password_hash(user.password, user_data['password']):
            raise BadRequest("Invalid email or password")

        return user



    @staticmethod
    def encode_token(user):
        payload = {
            "sub": user.id,
            "exp": datetime.now(UTC) + timedelta(days=10)
        }
        return jwt.encode(payload, config('SECRET_KEY'), algorithm='HS256')


    @staticmethod
    def decode_token(token):
        try:
            return jwt.decode(token, config('SECRET_KEY'), algorithms=['HS256'])
        except (DecodeError, InvalidSignatureError):
            raise BadRequest('Invalid or missing token')



auth = HTTPTokenAuth(scheme='Bearer')

@auth.verify_token
def verify_token(token):
    try:
        payload = AuthManager.decode_token(token)
        user = UserModel.query.filter_by(id=payload['sub']).first()
        if not user:
            raise Unauthorized('Invalid token or missing token')
        return user
    except Exception:
        raise Unauthorized('Invalid token or missing token')

