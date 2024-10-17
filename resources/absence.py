from flask import request
from flask_restful import Resource

from managers.absence import AbsenceManager
from managers.auth import auth
from models import UserType
from schemas.request.absence import AbsenceRequestSchema
from schemas.response.absence import AbsenceErrorResponse, AbsenceResponse
from utils.decorators import validate_schema, permission_required


class AbsenceRegisterResource(Resource):
    @validate_schema(AbsenceRequestSchema)
    def post(self):
        data = request.get_json()
        result, ok = AbsenceManager.create_absence(data)
        if not ok:
            return AbsenceErrorResponse().dump(result), result.error_code
        return AbsenceResponse().dump(result)

class AbsenceApproveResource(Resource):
    @auth.login_required
    @permission_required([UserType.accountant,UserType.manager])
    def get(self, absence_id):
        AbsenceManager.approve_absence(absence_id)


class AbsenceRejectResource(Resource):
    @auth.login_required
    @permission_required([UserType.manager, UserType.accountant])
    def get(self, absence_id):
        AbsenceManager.reject_absence(absence_id)