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


if __name__ == '__main__':
    app.debug=True
    app.run(
        host='0.0.0.0',
        port=5000
    )
