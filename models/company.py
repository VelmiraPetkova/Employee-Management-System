from datetime import datetime,  UTC

from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import  db



class CompanyModel(db.Model):
    __tablename__ = 'company'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    country: Mapped[str] = mapped_column(db.String(50), nullable=False, unique=True)
    address: Mapped[str] = mapped_column(db.String(50), nullable=False, unique=True)
    created_on: Mapped[datetime] = mapped_column(default=datetime.now(UTC))
    updated_on: Mapped[datetime] = mapped_column(onupdate=func.now(), default=datetime.now(UTC))
    #license_number


