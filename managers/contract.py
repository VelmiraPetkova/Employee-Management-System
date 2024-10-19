from flask import jsonify
from marshmallow import ValidationError
from sqlalchemy.sql.functions import current_user
from werkzeug.exceptions import BadRequest, NotFound

from db import db
from managers.auth import auth
from models import ContractsModel, UserModel, UserType
from services.SES import SEService
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

        #todo this is not work??
        if contract_data.get('contract_type')== 'permanent' or contract_data.get('contract_type')== 'ContractType.permanent' and contract_data.get('end_date') is not None:
            return CustomError('If you have a contract end date, change its type', 400), False

        # Find the user by the provided employee
        employee_id = contract_data.get('employee')
        employee = UserModel.query.get(employee_id)
        if not employee:
            return CustomError('Please register the user in the system first', 400), False


        contract = ContractsModel(**contract_data)
        name = employee.name
        recipient = employee.email


        db.session.add(contract)
        db.session.commit()

        SEService().send_email(name, recipient)

        return contract, True


role_mapper = {
             UserType.employee : ManagerContract._get_contract_by_employee,
             UserType.manager : ManagerContract._get_contract_by_manager,
             UserType.accountant : ManagerContract._get_contract_by_accountant
               }


class ContractChangeManager:
    @staticmethod
    def check_contract_id(contract_id):
        try:
            contract = ContractsModel.query.filter_by(id=contract_id).first()
        except (BadRequest, NotFound):
            raise BadRequest('No such contract exists')
        return contract

    @staticmethod
    def change_contract(contract_id, contract_data):
        contract=ContractChangeManager.check_contract_id(contract_id)
        for key, value in contract_data.items():
            if hasattr(contract, key):
                setattr(contract, key, value)
        db.session.commit()
        return contract


