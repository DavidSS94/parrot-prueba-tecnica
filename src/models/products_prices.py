from flask import g

from typing import Optional

from sqlalchemy import ForeignKey, Double, String, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base
from src.models.products import Product

class Products_prices(Base):
    __tablename__ = "products_prices"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )
    product_id: Mapped[str] = mapped_column(
        ForeignKey("products.id")
    )
    price: Mapped[float] = mapped_column(
        Double,
        nullable=False
    )
    start_date: Mapped[str] = mapped_column(
        DateTime,
        nullable=False
    )
    end_date: Mapped[str] = mapped_column(
        DateTime,
        nullable=False
    )

    def __init__(
            self,
            body: Optional[dict] = {}
        ) -> None:

        if body:
            for key in body.keys():
                if key == "product_name":
                    setattr(Products_prices, 'product_id', Product().get_pk(body[key]))
                else:
                    setattr(Products_prices, key, body[key])

    def create(self):
        try:
            g.session.add(self)
            g.session.commit()
            return 200, "Precio de producto registrado"
        
        except Exception as error:
            print(error.args[0])
            return 500, error.args[0]

    
    def get_all(self) -> list[Integer, String, list[dict]]:

        data = []
        try:
            products_price = g.session.query(Products_prices).all()

            for product_price in products_price:
                product = Product().get_by_id(product_price.id)

                data.append({
                    'product': product.name,
                    'price': product_price.price,
                    'start_date': product_price.start_date,
                    'end_date': product_price.end_date
                })

            return 200, "", data
        except Exception as error:
            print(error.args[0])
            return 500, error.args[0], data
