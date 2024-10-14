from enum import Enum


class UserType(Enum):
    accountant = "accountant"
    manager = "manager"
    employee = "employee"


class ContractType(Enum):
    permanent  = "permanent"
    temporary  = "temporary"
    civil  = "civil"