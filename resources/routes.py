from resources.absence import AbsenceRegisterResource, AbsenceApproveResource, AbsenceRejectResource, \
    AbsenceDeleteResource
from resources.auth import UserRegisterResource, UserLoginResource, AddManagerResource
from resources.contract import ContractsResource, ContractChangeResource

routes=(
    (UserRegisterResource, '/register'),
    (UserLoginResource, '/login'),
    (ContractsResource, '/contract'),
    (AbsenceRegisterResource, '/absenceregister'),
    (AddManagerResource,'/addmanager/user/<int:user_id>'),
    (AbsenceApproveResource, '/absences/<int:absence_id>/approve'),
    (AbsenceRejectResource,'/absences/<int:absence_id>/reject'),
    (ContractChangeResource, '/change/<int:contract_id>/contract'),
    (AbsenceDeleteResource,'/absences/<int:absence_id>/delete'),
)