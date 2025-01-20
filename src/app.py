from flask import Flask, jsonify, g, request
from flask_cors import CORS

import json

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

    g.classes = {
        'waiters': Waiter,
        'products': Product,
        'reports': Reports,
        'orders': Orders,
        'products_prices': Products_prices
    }


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

def get_data_file(file):
    with open(f"data/{file}.json", "r") as data:
        return json.load(data)


@app.route("/fill_tables", methods=["GET"])
def fill_tables():
    response = {
        "message": "Datos insertados con éxito",
        "code": 200
    }

    models_data = {
        "waiters": get_data_file("waiters"),
        "orders": get_data_file("orders"),
        "products": get_data_file("products"),
        "products_prices": get_data_file("products_prices"),
    }

    for model in models_data.keys():
        object_list = []
        for data in models_data[model]:
            object_list.append(g.classes[model](data))
        
        g.classes[model]().create_many(object_list)
        print(f"Data insertada en {model}")

    return jsonify(response), response["code"]


from src.models.base import Base
from src.models.waiter import Waiter
from src.models.order import Orders
from src.models.products import Product
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

    return jsonify(response), response["code"]


@app.route("/create", methods=["PUT"])
def create():
    response = {
        "code": 200
    }
    body = request.json

    if 'model' not in body:
        response["message"] = "Internal error"
        response["details"] = "Defina el modelo solicitado"
        response["code"] = 500
        return jsonify(response), response["code"]
    
    model = body['model']

    if model not in g.classes:
        response["message"] = "Internal error"
        response["details"] = "El modelo solicitado no existe"
        response["code"] = 500
        return jsonify(response), response["code"]

    if 'params' not in body:
        response["message"] = "Internal error"
        response["details"] = "Defina los parametros solicitado"
        response["code"] = 500
        return jsonify(response), response["code"]

    params = body['params']

    (code, message) = g.classes[model](params).create()

    if code == 200:
        response['message'] = message
    else:
        response['message'] = "Internal error"
        response['details'] = message
        response['code'] = code

    return jsonify(response), response["code"]


@app.route("/get_all/<model>", methods=["GET"])
def get_all(model):
    response = {
        "code": 200
    }

    model = request.view_args['model']

    if model not in g.classes:
        response["message"] = "Internal error"
        response["details"] = "El modelo solicitado no existe"
        response["code"] = 500
        return jsonify(response), response["code"]

    (code, message, data) = g.classes[model]().get_all()

    if code == 200:
        response['data'] = data
    else:
        response['message'] = "Internal error"
        response['details'] = message
        response['code'] = code

    return jsonify(response), response["code"]


@app.route("/find/<model>/<filter>", methods=["GET"])
def get_id(model, filter):
    response = {
        "code": 200
    }

    model = request.view_args['model']

    if model not in g.classes:
        response["message"] = "Internal error"
        response["details"] = "El modelo solicitado no existe"
        response["code"] = 500
        return jsonify(response), response["code"]
    
    filter = request.view_args['filter']

    (code, message, data) = g.classes[model]().find_one(filter)

    if code == 200:
        response['data'] = data
    else:
        response['message'] = "Internal error"
        response['details'] = message
        response['code'] = code

    return jsonify(response), response["code"]


@app.route("/delete/<model>/<name>", methods=["DELETE"])
def delete(model, name):
    response = {
        "code": 200
    }

    model = request.view_args['model']

    if model not in g.classes:
        response["message"] = "Internal error"
        response["details"] = "El modelo solicitado no existe"
        response["code"] = 500
        return jsonify(response), response["code"]
    
    name = request.view_args['name']

    (code, message) = g.classes[model]().delete(name)

    if code == 200:
        response['message'] = message
    else:
        response['message'] = "Internal error"
        response['details'] = message
        response['code'] = code

    return jsonify(response), response["code"]


@app.route("/update/<model>/<name>", methods=["PATCH"])
def update(model, name):
    response = {
        "code": 200
    }

    model = request.view_args['model']

    if model not in g.classes:
        response["message"] = "Internal error"
        response["details"] = "El modelo solicitado no existe"
        response["code"] = 500
        return jsonify(response), response["code"]
    
    name = request.view_args['name']
    body = request.json

    if not hasattr(g.classes[model](), "update"):
        response['message'] = "Internal error"
        response['details'] = "El modelo solicitado no puede realizar esta operación"
        response['code'] = 500

        return jsonify(response), response["code"]

    (code, message) = g.classes[model]().update(name, body)

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
