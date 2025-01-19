from flask import g

from typing import Optional
from datetime import datetime

from sqlalchemy import ForeignKey, DateTime, String, Integer, cast, Date
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
    date: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.now()
    )
    commensal_name: Mapped[str] = mapped_column(String, nullable=False)

    def __init__(
            self,
            body: Optional[dict] = {}
        ) -> None:
        
        if 'waiter_email' not in body or 'commensal_name' not in body:
            return 500, "La orden debe de tener waiter_email y commensal_name"
        
        self.waiter_email = body['waiter_email']
        self.commensal_name = body['commensal_name']


    def create(self) -> tuple[Integer, String]:

        try:
            g.session.add(self)
            g.session.commit()
            return 200, "Orden registrada"
        
        except Exception as error:
            print(error.args[0])
            return 500, error.args[0]


    def get_all(self) -> list[Integer, String, list[dict]]:

        data = []
        try:
            orders = g.session.query(Orders).all()

            for order in orders:
                data.append({
                    "waiter_email": order.waiter_email,
                    "commensal_name": order.commensal_name,
                    "date": order.date
                })
            return 200, "", data

        except Exception as error:
            print(error.args[0])
            return 500, error.args[0], data


    def find_one(
            self,
            filter: DateTime
        ) -> list[Integer, String, dict]:

        data = {}
        try:
            order = g.session.query(Orders).filter(
                cast(Orders.date, Date) == filter
            ).first()

            if order:
                data['commensal_name'] = order.commensal_name
                data['waiter_email'] = order.waiter_email
                data['date'] = order.date
                return 200, "", data

            else:
                return 500, "La fecha solicitada no cuenta con ordenes registradas", data

        except Exception as error:
            print(error.args[0])
            return 500, error.args[0], data


    def update(
            self,
            id: String,
            body: dict
        ) -> tuple[Integer, String]:

        try:
            pk = self.get_pk(id)

            order = g.session.query(Orders).filter(
                Orders.id == pk
            ).first()

            for key in body.keys():
                setattr(order, key, body[key])

            g.session.add(order)
            g.session.commit()

            return 200, "Orden actualizada"

        except Exception as error:
            print(error.args[0])
            return 500, error.args[0]


    def delete(
            self,
            id: String
        ) -> tuple[Integer, String]:

        try:
            pk = self.get_pk(int(id))

            if not pk == None:
                g.session.query(Orders).filter(
                    Orders.id == int(pk)
                ).delete()
                g.session.commit()
                return 200, "Orden borrada con exito"

            return 500, "La orden solicitada no fue encontrado"

        except Exception as error:
            print(error.args[0])
            return 500, error.args[0]


    def get_pk(
            self,
            id: Integer
        ) -> Integer:

        try:
            order = g.session.query(Orders.id).filter(
                Orders.id == id
            ).first()

            if order:
                return order.id

            else:
                return None

        except Exception as error:
            print(error.args[0])
