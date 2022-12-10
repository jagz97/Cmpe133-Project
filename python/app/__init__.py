import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_uploads import IMAGES, UploadSet, configure_uploads

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)



app.config.from_mapping(
    SECRET_KEY='you-will-never-know',
    SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(basedir, 'test.db'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)
photos = UploadSet('photos',IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/images')
configure_uploads(app, photos)

db = SQLAlchemy(app)

login = LoginManager(app)
login.login_view = 'login'

from app import server