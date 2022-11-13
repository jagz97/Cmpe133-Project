
import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

BASE_DIR = os.path.dirname(os.path.realpath(__file__))


class BaseConfig():

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'apidata.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "flask-app-secret-key-change-it"
    JWT_SECRET_KEY = "jwt-app-secret-key-change-it"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)