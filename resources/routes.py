from resources.absence import AbsenceRegisterResource, AbsenceApproveResource, AbsenceRejectResource
from resources.auth import UserRegisterResource, UserLoginResource, AddManagerResource
from resources.contract import ContractsResource

routes=(
    (UserRegisterResource, '/register'),
    (UserLoginResource, '/login'),
    (ContractsResource, '/contract'),
    (AbsenceRegisterResource, '/absenceregister'),
    (AddManagerResource,'/addmanager/user/<int:user_id>'),
    (AbsenceApproveResource, '/absences/<int:absence_id>/approve'),
    (AbsenceRejectResource,'/absences/<int:absence_id>/reject')
)