from datetime import date

from sqlalchemy import  ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import  db
from models.enums import AbsenceType


class AbsenceModel(db.Model):
    __tablename__ = 'absences'
    id: Mapped[int] = mapped_column(primary_key=True)
    from_: Mapped[date] = mapped_column(db.Date, nullable=True)
    to_: Mapped[date] = mapped_column(db.Date, nullable=True)
    days: Mapped[int] = mapped_column(db.Integer, nullable=True)
    type: Mapped[AbsenceType] = mapped_column(
        db.Enum(AbsenceType),  nullable=True
    )
    employee: Mapped[int] = mapped_column(db.Integer, nullable=True)
    photo: Mapped[str] = mapped_column(db.String, nullable=True)

    contracts_id: Mapped[int] = mapped_column(db.Integer, ForeignKey('contracts.id'), nullable=True)
    contract: Mapped['ContractsModel'] = relationship('ContractsModel')

    # TO DO: this is must be approved
