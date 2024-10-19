from datetime import datetime, UTC


from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column


from models.enums import UserType
from db import  db


class UserModel(db.Model):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    civil_number: Mapped[str] = mapped_column(db.String(10), nullable=False, unique=True)
    address: Mapped[str] = mapped_column(db.String(255), nullable=True, server_default="Undefined",default="Undefined")
    phone: Mapped[str] = mapped_column(db.String(10), nullable=False)
    email: Mapped[str] = mapped_column(db.String(100), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(db.String(200), nullable=False)
    iban: Mapped[str] = mapped_column(db.String(22), nullable=False, unique=True)
    created_on: Mapped[datetime] = mapped_column(default=datetime.now(UTC))
    updated_on: Mapped[datetime] = mapped_column(onupdate=func.now(), default=datetime.now(UTC))
    date_birth: Mapped[str] = mapped_column(db.String(10), server_default="Undefined", default="Undefined")
    manager :Mapped[int] = mapped_column(db.Integer, nullable=True)
    emergency_contact:Mapped[str] = mapped_column(db.String(50), nullable=True)
    role: Mapped[UserType] = mapped_column(
        db.Enum(UserType), default=UserType.employee.name, nullable=False
    )

    #contracts = db.relationship('ContractsModel', back_populates='user')