from typing import Optional
from datetime import datetime

from sqlalchemy import ForeignKey, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base

from src.models.base import Base

class Orders(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        unique=True
    )
    waiter_email: Mapped[str] = mapped_column(
        ForeignKey("waiters.email"),
        primary_key=True
    )
    date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    commensal_name: Mapped[str] = mapped_column(String, nullable=False)

