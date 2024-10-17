from flask import jsonify
from marshmallow import ValidationError
from sqlalchemy.sql.functions import current_user

from db import db
from managers.auth import auth
from models import ContractsModel, UserModel, UserType
from utils.missing_required_field_error import CustomError



class ManagerContract:
    @staticmethod
    def get_contracts():
        role = auth.current_user().role
        contracts = role_mapper[role]()
        return contracts

    @staticmethod
    def _get_contract_by_accountant():
        ContractsModel.query.filter_by().all()

    @staticmethod
    def _get_contract_by_employee():
        current_user = auth.current_user()
        return ContractsModel.query.filter_by(user_id = current_user.id).all()

    @staticmethod
    def _get_contract_by_manager():
        current_user = auth.current_user()
        return ContractsModel.query.filter_by(manager = current_user.id).all()

    @staticmethod
    def create_contract(contract_data):
        user = auth.current_user()
        contract_data['user_id'] = user.id

        if contract_data.get('contract_type')== 'temporary' and contract_data.get('end_date') is None:
            return CustomError('End date cannot be empty when contract is temporary', 400), False

        # Find the user by the provided employee
        employee_id = contract_data.get('employee')
        employee = UserModel.query.get(employee_id)
        if not employee:
            return CustomError('Please register the user in the system first', 400), False

        contract = ContractsModel(**contract_data)
        db.session.add(contract)
        db.session.commit()
        return contract, True


role_mapper = {
             UserType.employee : ManagerContract._get_contract_by_employee,
             UserType.manager : ManagerContract._get_contract_by_manager,
             UserType.accountant : ManagerContract._get_contract_by_accountant
               }