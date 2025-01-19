from flask import Flask, jsonify, g, request
from flask_cors import CORS

app = Flask(__name__)
CORS(
    app,
    resources={
        r"/*": {
            "methods": [ "*" ]
        }
    }
)


from src.tools.sql import get_engine, get_session
@app.before_request
def before_request():
    g.engine = get_engine()
    g.session = get_session(g.engine)

@app.route("/", methods=["GET"])
def hello_word():
    response = {
        "message": "Hello Word",
        "code": 200
    }

    return jsonify(response), response["code"]

from src.tools.sql import create_db
@app.route("/define_database", methods=["GET"])
def define_database():
    response = {
        "code": 200
    }

    [code, message] = create_db()

    response["code"] = code
    if code == 200:
        response["message"] = message
    else:
        response["message"] = "Internal error"
        response["details"] = message

    return jsonify(response), response["code"]


from src.models.base import Base
from src.models.waiter import Waiter
from src.models.order import Orders
from src.models.products import Products
from src.models.products_prices import Products_prices
from src.models.report import Reports
@app.route("/define_models", methods=["GET"])
def create_tables():
    response = {
        "code": 200
    }

    try:
        Base.metadata.create_all(g.engine)
        response["message"] = "Tablas creadas con éxito"

    except Exception as error: 
        response["message"] = "Error al crear las tablas"
        response["details"] = error.args[0]
        response["code"] = 500

    return jsonify(response), response["code"]


@app.route("/waiters/create", methods=["PUT"])
def create_waiter():
    response = {
        "code": 200
    }
    body = request.json

    (code, message) = Waiter(body).create()

    if code == 200:
        response['message'] = message
    else:
        response['message'] = "Error al registrar al mesero"
        response['details'] = message
        response['code'] = code

    return jsonify(response), response["code"]


@app.route("/waiters/read", methods=["GET"])
def get_waiter_all():
    response = {
        "code": 200
    }

    (code, message, data) = Waiter().get_all()

    if code == 200:
        response['data'] = data
    else:
        response['message'] = "Error al registrar al mesero"
        response['details'] = message
        response['code'] = code

    return jsonify(response), response["code"]


@app.route("/waiters/read/<name>", methods=["GET"])
def get_waiter_id(name):
    response = {
        "code": 200
    }

    name = request.view_args['name']

    (code, message, data) = Waiter().find_one(name)

    if code == 200:
        response['data'] = data
    else:
        response['message'] = "Internal error"
        response['details'] = "El mesero solicitado no existe"
        response['code'] = code

    return jsonify(response), response["code"]


@app.route("/waiters/delete/<name>", methods=["DELETE"])
def delete_waiter(name):
    response = {
        "code": 200
    }

    name = request.view_args['name']

    (code, message) = Waiter().delete(name)

    if code == 200:
        response['message'] = message
    else:
        response['message'] = "Internal error"
        response['details'] = message
        response['code'] = code

    return jsonify(response), response["code"]


@app.route("/waiters/update/<name>", methods=["PATCH"])
def update_waiter(name):
    response = {
        "code": 200
    }

    name = request.view_args['name']
    body = request.json

    (code, message) = Waiter().update(name, body)

    if code == 200:
        response['message'] = message
    else:
        response['message'] = "Internal error"
        response['details'] = message
        response['code'] = code

    return jsonify(response), response["code"]


if __name__ == '__main__':
    app.debug=True
    app.run(
        host='0.0.0.0',
        port=5000
    )
