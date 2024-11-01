from flask_restful import Resource

from flask import request, jsonify
from marshmallow import ValidationError
from werkzeug.exceptions import BadRequest

from db import db
from managers.auth import auth
from managers.contract import ManagerContract, ContractChangeManager
from models import ContractsModel, UserType
from schemas.request.contract import RequestContractSchema, ChangeContractSchema
from schemas.response.contract import ContractResponse, ContractErrorResponse
from utils.decorators import validate_schema, permission_required


class ContractsResource(Resource):
    @auth.login_required
    def get(self):
        user = auth.current_user()
        contracts = ManagerContract.get_contracts(user)
        return ContractResponse().dump(contracts, many=True)


    @auth.login_required
    @permission_required([UserType.accountant])
    @validate_schema(RequestContractSchema)
    def post(self):
        data = request.get_json()
        result = ManagerContract.create_contract(data)
        return ContractResponse().dump(result),201


class ContractChangeResource(Resource):
    @auth.login_required
    @permission_required([UserType.accountant, UserType.manager])
    @validate_schema(ChangeContractSchema)
    def put(self, contract_id):
        data = request.get_json()
        contract= ContractChangeManager.change_contract(contract_id, data)
        return ContractResponse().dump(contract)
