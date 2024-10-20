import os.path
import uuid
from datetime import datetime


from werkzeug.exceptions import BadRequest

from constants import ROOT_DIR, TEMP_FILES_PATH
from managers.auth import auth
from models.enums import  State
from db import db
from models import ContractsModel, AbsenceModel
from services.s3 import S3Service

from utils.working_with_files import decode_photo


s3_service = S3Service()

class AbsenceManager:
    @staticmethod
    def take_contract(employee=None):

        if employee is not None:
            try:
                contract= ContractsModel.query.filter_by(employee=employee).first()
            except Exception as ex:
                raise Exception(f"No contract found for employee with ID {employee}")
        else:
            user = auth.current_user()
            contract= ContractsModel.query.filter_by(employee=user.id).first()

        try:
            if contract.contract_type != 'civil':
                return contract
        except Exception as ex:
            raise Exception("Your contract is not eligible for absence")

        return contract


    @staticmethod
    def check_date(date_from, date_to):
        # Convert string to date
        try:
            from_date = datetime.strptime(date_from, "%Y-%m-%d").date()
            to_date = datetime.strptime(date_to, "%Y-%m-%d").date()
        except Exception as ex:
            raise Exception("Invalid date format. Use YYYY-MM-DD.")
        return from_date, to_date


    @staticmethod
    def create_absence(absence_data):
        employee = absence_data.get('employee')
        contract = absence_data.get('contracts_id')
        if contract is None:
            contract= AbsenceManager.take_contract(employee)

        days = absence_data.get('days')
        type_absence = absence_data.get('type')
        contract_start_date = contract.effective
        # Ensure that the absence period falls within the contract period
        try:
            from_date, to_date= AbsenceManager.check_date(absence_data.get('from_'), absence_data.get('to_'))
            if contract_start_date <= from_date:
                pass
        except Exception as ex:
            raise Exception("The absence dates are not within the active contract period.")

        # Work with photo before create absence
        if absence_data.get('photo_extension') and absence_data.get('photo') is not None:

            photo_name = f"{str(uuid.uuid4())}.{absence_data.pop('photo_extension')}"
            path_to_store_photo= os.path.join(TEMP_FILES_PATH, photo_name)
            photo= absence_data.pop('photo')
            decode_photo(path_to_store_photo, photo)

            try:
                bucket_url = s3_service.upload_file(path_to_store_photo, os.path.basename(path_to_store_photo))
            except Exception as ex:
                raise Exception("Upload to s3 failed")
            finally:
                os.remove(path_to_store_photo)


            absence_data["photo"] = bucket_url

        absence = AbsenceModel(**absence_data)
        db.session.add(absence)
        db.session.commit()
        return absence


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

    @staticmethod
    def delete_absence(absence_id):
        current_absence = AbsenceModel.query.filter_by(id=absence_id).first()
        curr_user = auth.current_user().id
        if curr_user != current_absence.employee:
            raise BadRequest("Can not delete absence!")

        current_absence.delete()



