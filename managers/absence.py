from datetime import datetime, date

from alembic.util import status
from flask import jsonify
from werkzeug.exceptions import BadRequest

from models.enums import  State
from db import db
from models import ContractsModel, AbsenceModel
from utils.missing_required_field_error import CustomError


class AbsenceManager:
    @staticmethod
    def create_absence(absence_data):

        # Convert string to date
        try:
            from_date = datetime.strptime(absence_data.get('from_'), "%Y-%m-%d").date()
            to_date = datetime.strptime(absence_data.get('to_'), "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

        days = absence_data.get('days')
        employee = absence_data.get('employee')
        type_absence = absence_data.get('type')
        contract_id = absence_data.get('contracts_id')

        if contract_id is None:
            try:
                # Fetch contract associated with the employee
                contract = ContractsModel.query.filter_by(employee=employee).first()
                if contract is None:
                    return CustomError (f"No contract found for employee with ID {employee}"), False
            finally:
                contract_id = contract.id


        absence_data['contracts_id'] = contract_id
        contract = ContractsModel.query.filter_by(id=contract_id).first()
        contract_start_date = contract.effective
        #contract_end_date = datetime.strptime(contract.end_date, "%Y-%m-%d").date()


            # Ensure that the absence period falls within the contract period
        if not (
                contract_start_date <= from_date and contract_start_date <= to_date):
            return CustomError ("The absence dates are not within the active contract period."), False


        absence = AbsenceModel(**absence_data)
        db.session.add(absence)
        db.session.commit()
        return absence, True


    @staticmethod
    def approve_absence(absence_id):
        AbsenceManager._validate_absence(absence_id)
        absence = AbsenceModel.query.filter_by(id=absence_id).update({"status": State.approved})
        db.session.commit()

    @staticmethod
    def reject_absence(absence_id):
        AbsenceManager._validate_absence(absence_id)
        absence = AbsenceModel.query.filter_by(id=absence_id).update({"status": State.rejected})
        db.session.commit()

    @staticmethod
    def _validate_absence(absence_id):
        absence = AbsenceModel.query.filter_by(id=absence_id).first()
        if not absence:
            raise BadRequest("Absence not found.")

        if absence.status != State.pending:
            raise BadRequest("Can not change status of absence.")