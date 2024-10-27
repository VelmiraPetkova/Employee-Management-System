from datetime import date, datetime
from shutil import Error

from flask import jsonify
from marshmallow import ValidationError
from sqlalchemy.sql.functions import current_user
from werkzeug.exceptions import BadRequest, NotFound, BadRequestKeyError

from db import db
from managers.auth import auth
from models import ContractsModel, UserModel, UserType
from services.SES import SEService
from utils.missing_required_field_error import CustomError



class ManagerContract:
    @staticmethod
    def get_contracts(role):
        user_rol = role.role
        #user_rol = auth.current_user().role
        contracts = role_mapper[user_rol]()
        return contracts

    @staticmethod
    def _get_contract_by_accountant():
        return ContractsModel.query.filter_by().all()

    @staticmethod
    def _get_contract_by_employee():
        current_user = auth.current_user()
        return ContractsModel.query.filter_by(employee = current_user.id).all()

    @staticmethod
    def _get_contract_by_manager():
        current_user = auth.current_user()
        return ContractsModel.query.filter_by(manager = current_user.id).all()

    @staticmethod
    def create_contract(contract_data):
        user = auth.current_user()
        contract_data['user_id'] = user.id

        if contract_data.get('contract_type')== 'temporary' and contract_data.get('end_date') is None:
            raise BadRequest ('End date cannot be empty when contract is temporary')


        if (contract_data.get('contract_type')== 'temporary'
                and datetime.strptime(contract_data.get('end_date'), "%Y-%m-%d").date() <= datetime.strptime(contract_data.get('effective'), "%Y-%m-%d").date()):
            raise BadRequest ('The end date cannot be less than the start date')

        if (contract_data.get('contract_type')== 'permanent'
                or contract_data.get('contract_type')== 'ContractType.permanent' and contract_data.get('end_date') is not None):
            raise BadRequest ('If you have a contract end date, change its type')


        employee_id = contract_data.get('employee')
        # Find the user by the provided employee
        employee = UserModel.query.filter_by(id=employee_id).first()
        if employee is None:
            raise  BadRequest('Please register the user in the system first!')


        if  datetime.strptime(contract_data.get('effective'), "%Y-%m-%d").date() <= date.today():
            raise BadRequest('Effective date must be greater than current date')

        contract = ContractsModel(**contract_data)
        name = employee.name
        recipient = employee.email

        db.session.add(contract)
        db.session.commit()
        SEService().send_email(name, recipient)

        return contract


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


