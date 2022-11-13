import json

from flask import Flask
from flask_cors import CORS

from .config import BaseConfig
from .routes import app_api
from .models import db

app = Flask(__name__)

app.config.from_object(BaseConfig)

db.init_app(app)
app_api.init_app(app)
CORS(app)


@app.before_first_request
def initialize_database():
    db.create_all()


@app.after_request
def after_request(response):
    """
       Sends back a custom error with {"success", "msg"} format
    """

    if int(response.status_code) >= 400:
        response_data = json.loads(response.get_data())
        if "errors" in response_data:
            response_data = {"success": False,
                             "msg": list(response_data["errors"].items())[0][1]}
            response.set_data(json.dumps(response_data))
        response.headers.add('Content-Type', 'application/json')
    return response