from datetime import datetime, timedelta , UTC


from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


from models.enums import UserType, ContractType
from db import  db


class UserModel(db.Model):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    civil_number: Mapped[str] = mapped_column(db.String(10), nullable=False, unique=True)
    address: Mapped[str] = mapped_column(db.String(255), nullable=True, server_default="Undefined",default="Undefined")
    phone: Mapped[str] = mapped_column(db.String(10), nullable=False)
    email: Mapped[str] = mapped_column(db.String(20), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(db.String(200), nullable=False)
    iban: Mapped[str] = mapped_column(db.String(22), nullable=False, unique=True)
    created_on: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_on: Mapped[datetime] = mapped_column(onupdate=func.now(), server_default=func.now())
    date_birth: Mapped[str] = mapped_column(db.String(10), server_default="Undefined", default="Undefined")
    manager :Mapped[int] = mapped_column(db.Integer, nullable=True)
    emergency_contact:Mapped[str] = mapped_column(db.String(50), nullable=True)
    role: Mapped[UserType] = mapped_column(
        db.Enum(UserType), default=UserType.employee.name, nullable=False
    )

    contract_id: Mapped[int] = mapped_column(ForeignKey("contracts.id"), nullable=True)
    #contract: Mapped['ContractsModel'] = relationship(back_populates='contract')

    company_id: Mapped[int] = mapped_column(ForeignKey("company.id"), nullable=True)
    #company: Mapped['CompanyModel'] = relationship(back_populates='company')



class CompanyModel(db.Model):
    __tablename__ = 'company'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    country: Mapped[str] = mapped_column(db.String(50), nullable=False, unique=True)
    address: Mapped[str] = mapped_column(db.String(50), nullable=False, unique=True)
    economic_activity_code: Mapped[int] = mapped_column(db.Integer, nullable=True)

    #users: Mapped[list['UserModel']] = relationship(back_populates='user')


class ContractsModel(db.Model):
    __tablename__ = 'contracts'
    id: Mapped[int] = mapped_column(primary_key=True)
    contract_date:Mapped[datetime] = mapped_column(db.DateTime, nullable=False)
    effective:Mapped[datetime] = mapped_column(db.DateTime, nullable=False)
    end_date:Mapped[datetime] = mapped_column(db.DateTime, nullable=True)
    salary:Mapped[int] = mapped_column(db.Integer, nullable=True)
    hours:Mapped[int] = mapped_column(db.Integer, nullable=True)
    contract_type:Mapped[ContractType] = mapped_column(
        db.Enum(ContractType), default=ContractType.permanent.name, nullable=False
    )

    #users: Mapped[list['UserModel']] = relationship(back_populates='user')





