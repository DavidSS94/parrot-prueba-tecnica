from flask import g

from typing import Optional

from sqlalchemy import ForeignKey, Integer, Boolean, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base

from src.models.base import Base
from src.models.order import Orders
from src.models.products_prices import Products_prices

class Reports(Base):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        unique=True
    )

    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id"),
        nullable=False
    )
    product_prices_id: Mapped[str] = mapped_column(
        ForeignKey("products_prices.id"),
        nullable=False
    )
    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )
    to_go: Mapped[bool] = mapped_column(
        Boolean,
        unique=False,
        default=False
    )

    def __init__(
            self,
            body: Optional[dict] = {}
        ) -> None:

        if body:
            for key in body.keys():
                if key == 'order_id':
                    order_id = Orders().get_by_pk(body[key])
                    setattr(self, key, order_id)
                
                if key == 'product_prices_id':
                    product_prices_id = Products_prices().get_by_pk(body[key])
                    setattr(self, key, product_prices_id)
                setattr(self, key, body[key])
                
                


    def create(self) -> tuple[Integer, String]:
        try:
            g.session.add(self)
            g.session.commit()
            
            return 200, "Reporte generado"
        
        except Exception as error:
            g.session.rollback()
            print(error.args[0])
            return 500, error.args[0]
