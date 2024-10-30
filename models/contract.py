from datetime import datetime, UTC, date

from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship



from models.enums import ContractType
from db import  db


class ContractsModel(db.Model):
    __tablename__ = 'contracts'
    id: Mapped[int] = mapped_column(primary_key=True)
    employee: Mapped[int] = mapped_column(db.Integer, nullable=False)
    created_on:Mapped[datetime] = mapped_column(default=datetime.now(UTC))
    updated_on: Mapped[datetime] = mapped_column(onupdate=func.now(), default=datetime.now(UTC))
    effective:Mapped[date] = mapped_column(db.Date, nullable=False)
    end_date:Mapped[date] = mapped_column(db.Date, nullable=True)
    salary:Mapped[float] = mapped_column(db.Float, nullable=True)
    hours:Mapped[float] = mapped_column(db.Float, nullable=True)
    position: Mapped[str] = mapped_column(db.String, nullable=False)
    department: Mapped[str] = mapped_column(db.String, nullable=False)

    contract_type:Mapped[ContractType] = mapped_column(
        db.Enum(ContractType), default = ContractType.permanent.name, nullable=False
    )

    # the user created the contract
    user_id: Mapped[int] = mapped_column(db.Integer,ForeignKey('users.id'), nullable=False)
    user: Mapped['UserModel'] = relationship('UserModel')

    #company_id: Mapped[int] = mapped_column(db.Integer,ForeignKey('company.id'),nullable=True)
    #company: Mapped["CompanyModel"] = relationship('CompanyModel')

