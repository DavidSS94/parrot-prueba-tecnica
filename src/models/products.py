from flask import g

from typing import Optional

from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base

from src.models.base import Base

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    type: Mapped[str] = mapped_column(String, nullable=False)

    def __init__(
            self,
            body: Optional[dict] = {}
        ) -> None:
        
        if 'name' not in body or 'type' not in body:
            return 500, "El producto debe de tener name y type"
        
        self.name = body['name']
        self.type = body['type']


    def create(self) -> tuple[Integer, String]:

        try:
            g.session.add(self)
            g.session.commit()
            return 200, "Producto registrado"
        
        except Exception as error:
            print(error.args[0])
            return 500, error.args[0]


    def get_all(self) -> list[Integer, String, list[dict]]:

        data = []
        try:
            products = g.session.query(Product).all()

            for product in products:
                data.append({
                    "name": product.name,
                    "type": product.type
                })
            return 200, "", data

        except Exception as error:
            print(error.args[0])
            return 500, error.args[0], data


    def find_one(
            self,
            name: String
        ) -> list[Integer, String, dict]:

        data = {}
        try:
            product = g.session.query(Product).filter(
                Product.name == name
            ).first()

            if hasattr(product, 'name'):
                data['name'] = product.name
                data['type'] = product.type
                return 200, "", data

            else:
                return 500, "El producto solicitado no fue encontrado", data

        except Exception as error:
            print(error.args[0])
            return 500, error.args[0], data


    def update(
            self,
            name: String,
            body: dict
        ) -> tuple[Integer, String]:

        try:
            pk = self.get_pk(name)

            product = g.session.query(Product).filter(
                Product.id == pk
            ).first()

            for key in body.keys():
                setattr(product, key, body[key])

            g.session.add(product)
            g.session.commit()

            return 200, "Producto actualizado"

        except Exception as error:
            print(error.args[0])
            return 500, error.args[0]


    def delete(
            self,
            name: String
        ) -> tuple[Integer, String]:

        try:
            pk = self.get_pk(name)

            if not pk == None:
                g.session.query(Product).filter(
                    Product.id == pk
                ).delete()
                g.session.commit()
                return 200, "Producto borrado con exito"

            return 500, "El producto solicitado no fue encontrado"

        except Exception as error:
            print(error.args[0])
            return 500, error.args[0]
    

    def get_pk(
            self,
            name: String
        ) -> String:

        try:
            product = g.session.query(Product).filter(
                Product.name == name
            ).first()

            if hasattr(product, 'id'):
                return product.id

            else:
                return None

        except Exception as error:
            print(error.args[0])
