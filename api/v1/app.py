#!/usr/bin/python3
""" api for AirBnB """
from flask import Flask
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


if __name__ == "__main__":
    """ maind method for flask app """
    app.run(host=host, port=port, threaded=True)
