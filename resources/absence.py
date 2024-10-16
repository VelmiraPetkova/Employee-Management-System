from flask import request
from flask_restful import Resource

from managers.absence import AbsenceManager
from schemas.request.absence import AbsenceRequestSchema
from schemas.response.absence import AbsenceErrorResponse, AbsenceResponse
from utils.decorators import validate_schema


class AbsenceRegisterResource(Resource):
    @validate_schema(AbsenceRequestSchema)
    def post(self):
        data = request.get_json()
        result, ok = AbsenceManager.create_absence(data)
        if not ok:
            return AbsenceErrorResponse().dump(result), result.error_code
        return AbsenceResponse().dump(result)