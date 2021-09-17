#!/usr/bin/python3
""" api for AirBnB """
from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
import os

host = os.getenv('HBNB_API_HOST', '0.0.0.0')
port = os.getenv('HBNB_API_PORT', 5000)

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """ remove the curretn SQLAlchemy """
    storage.close()


@app.errorhandler(404)
def handle_404(error):
    """ a method handler for 404 erros that returns a JSON-formated 404 status
    code response with content error: Not found
    """
    content = {"error": "Not found"}
    return make_response(jsonify(content), 404)


if __name__ == "__main__":
    """ maind method for flask app """
    app.run(host=host, port=port, threaded=True)
