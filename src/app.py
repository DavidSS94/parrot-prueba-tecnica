from flask import Flask, jsonify
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
        "message": "",
        "code": 0
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
from src.tools.sql import get_engine, get_session
from src.models import waiter, order, products, products_prices, report
@app.route("/define_models", methods=["GET"])
def create_tables():
    response = {
        "message": "",
        "code": 200
    }

    engine = get_engine()
    session = get_session(engine)
    try:
        Base.metadata.create_all(engine)
        response["message"] = "Tablas creadas con éxito"

    except Exception as error: 
        response["message"] = "Error al crear las tablas"
        response["details"] = error.args[0]
        response["code"] = 500

    session.close()

    return jsonify(response), response["code"]


if __name__ == '__main__':
    app.debug=True
    app.run(
        host='0.0.0.0',
        port=5000
    )
