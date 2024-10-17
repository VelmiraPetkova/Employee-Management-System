from enum import Enum


class UserType(Enum):
    accountant = "accountant"
    manager = "manager"
    employee = "employee"


class ContractType(Enum):
    permanent  = "permanent"
    temporary  = "temporary"
    civil  = "civil"


class AbsenceType(Enum):
    sick = "sick"
    paid  = "paid"
    unpaid = "unpaid"


class State(Enum):
    pending = "Pending"
    approved = "Approved"
    rejected = "Rejected"