import os.path
import uuid
from datetime import datetime, date

from flask import jsonify
from werkzeug.exceptions import BadRequest

from constants import ROOT_DIR, TEMP_FILES_PATH
from managers.auth import auth
from models.enums import  State
from db import db
from models import ContractsModel, AbsenceModel
from services.s3 import S3Service
from utils.missing_required_field_error import CustomError
from utils.working_with_files import decode_photo


s3_service = S3Service()

class AbsenceManager:
    @staticmethod
    def validate_type_contract():
        user = auth.current_user()
        contract = ContractsModel.query.filter_by(employee=user.id).first()
        return contract


    @staticmethod
    def create_absence(absence_data):
        contract_type= AbsenceManager.validate_type_contract().contract_type
        if contract_type == 'civil':
            return CustomError("Your contract is not eligible for absence"), False


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
            return CustomError("The absence dates are not within the active contract period."), False


        #Work with photo before create absence
        photo_name = f"{str(uuid.uuid4())}.{absence_data.pop('photo_extension')}"
        path_to_store_photo= os.path.join(TEMP_FILES_PATH, photo_name)
        photo= absence_data.pop('photo')
        decode_photo(path_to_store_photo, photo)

        try:
            bucket_url= s3_service.upload_file(path_to_store_photo, photo)
        except Exception as ex:
            raise Exception("Upload to s3 failed")
        finally:
            os.remove(path_to_store_photo)


        absence_data["photo"] = bucket_url

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