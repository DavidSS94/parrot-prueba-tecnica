from typing import Optional

from flask import g

from sqlalchemy import select
from sqlalchemy import String, Tuple, Integer
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base

class Waiter(Base):
    __tablename__ = "waiters"

    email: Mapped[str] = mapped_column(
        primary_key=True,
        unique=True
    )
    name: Mapped[str] = mapped_column(String, nullable=False)

    def __init__(
            self,
            body: Optional[dict] = {}
        ):

        if 'email' not in body or 'name' not in body:
            return 500, "El waiter debe de tener Email o Name"

        self.email = body['email']
        self.name = body['name']


    def create(self) -> tuple[Integer, String]:

        try:
            g.session.add(self)
            g.session.commit()
            return 200, "Mesero registrado"

        except Exception as error:
            print(error.args[0])
            return 500, error.args[0]


    def create_many(self, data: list[object]) -> tuple[Integer, String]:

        try:
            g.session.add_all(data)
            g.session.commit()
            return 200, "Meseros registrados"

        except Exception as error:
            print(error.args[0])
            return 500, error.args[0]


    def get_all(self):
        data = []
        try:
            waiters = g.session.query(Waiter).all()

            for waiter in waiters:
                data.append({
                    "email": waiter.email,
                    "name": waiter.name
                })
            return 200, "", data

        except Exception as error:
            print(error.args[0])
            return 500, error.args[0], data


    def find_one(
            self,
            name: String
        ):

        data = {}

        try:
            waiter = g.session.query(Waiter).filter(
                Waiter.name == name
            ).first()

            if hasattr(waiter, 'email'):
                data['email'] = waiter.email
                data['name'] = waiter.name
                return 200, "", data

            else:
                return 500, "El mesero solicitado no fue encontrado", data

        except Exception as error:
            print(error.args[0])
            return 500, error.args[0], data


    def delete(
            self,
            name: String
        ):

        try:
            pk = self.get_pk(name)

            if not pk == None:
                g.session.query(Waiter).filter(
                    Waiter.email == pk
                ).delete()
                g.session.commit()
                return 200, "Mesero borrado con exito"

            return 500, "El mesero solicitado no fue encontrado"

        except Exception as error:
            print(error.args[0])
            return 500, error.args[0]


    def get_pk(
            self,
            name: String
        ):

        data = {}

        try:
            waiter = g.session.query(Waiter).filter(
                Waiter.name == name
            ).first()

            if hasattr(waiter, 'email'):
                return waiter.email

            else:
                return None

        except Exception as error:
            print(error.args[0])
