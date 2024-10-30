from werkzeug.exceptions import BadRequest, NotFound

from db import db
from models import UserModel



class UserManager:
    """It is used to check the user from the request if it exists"""
    @staticmethod
    def _verify_user(user_id):
        try:
            change_user = UserModel.query.get(user_id)
        except (BadRequest, NotFound):
            raise BadRequest('No such user found')

        return change_user

    @staticmethod
    def _check_manager(put_data):
        manager = UserModel.query.filter_by(id=put_data.get('manager')).first()
        if manager is None:
            raise BadRequest('No such manager exists')
        else:
            return manager.id


    @staticmethod
    def assign_manager(data,user_id):
        user = UserManager._verify_user(user_id)
        manager_id = UserManager._check_manager(data)
        user.manager = manager_id
        db.session.commit()
        return user
