from resources.absence import AbsenceRegisterResource
from resources.auth import UserRegisterResource, UserLoginResource
from resources.contract import ContractsResource

routes=(
    (UserRegisterResource, '/register'),
    (UserLoginResource, '/login'),
    (ContractsResource, '/contract'),
    (AbsenceRegisterResource, '/absenceregister'),
)