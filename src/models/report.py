from typing import Optional

from sqlalchemy import ForeignKey, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base

from src.models.base import Base

class Reports(Base):
    __tablename__ = "reports"

    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id"),
        primary_key=True
    )
    product_prices_id: Mapped[str] = mapped_column(
        ForeignKey("products_prices.id"),
        primary_key=True
    )
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    to_go: Mapped[bool] = mapped_column(Boolean, nullable=False)

