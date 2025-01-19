from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base

class Waiter(Base):
    __tablename__ = "waiters"

    email: Mapped[str] = mapped_column(
        primary_key=True,
        unique=True
    )
    name: Mapped[str] = mapped_column(String, nullable=False)

    def __self__(self):
        return self.email

