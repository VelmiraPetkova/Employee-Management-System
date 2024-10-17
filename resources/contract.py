from flask_restful import Resource

from flask import request, jsonify

from db import db
from managers.auth import auth
from managers.contract import ManagerContract
from models import ContractsModel, UserType
from schemas.request.contract import RequestContractSchema
from schemas.response.contract import ContractResponse, ContractErrorResponse
from utils.decorators import validate_schema, permission_required


class ContractsResource(Resource):
    @auth.login_required
    def get(self):
        contracts = ManagerContract.get_contracts()
        return ContractResponse(many=True).dump(contracts)


    @auth.login_required
    @permission_required([UserType.accountant])
    @validate_schema(RequestContractSchema)
    def post(self):
        data = request.get_json()
        result, ok = ManagerContract.create_contract(data)
        if not ok:
            return ContractErrorResponse().dump(result), result.error_code
        return ContractResponse().dump(result)
