from typing import Optional

from sqlalchemy import ForeignKey, Float, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base

from src.models.base import Base

class Products_prices(Base):
    __tablename__ = "products_prices"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )
    product_id: Mapped[str] = mapped_column(
        ForeignKey("products.id")
    )
    price: Mapped[float] = mapped_column(Float, nullable=False)
    start_date: Mapped[str] = mapped_column(String, nullable=False)
    end_date: Mapped[str] = mapped_column(String, nullable=False)

