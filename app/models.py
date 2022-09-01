from sqlalchemy import Column, ForeignKey, false
from app import db
from datetime import datetime
from flask_login import UserMixin
from app import login
from werkzeug.security import generate_password_hash, check_password_hash
import json


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True, nullable=False, unique=True)
    email = db.Column(db.String(32), index=True, nullable=False, unique=True)
    password_hash = db.Column(db.String(300), nullable=False)
    full_name = db.Column(db.String(128))
    address_line_one = db.Column(db.String(256))
    address_line_two = db.Column(db.String(256))
    city = db.Column(db.String(128))
    state_province_region = db.Column(db.String(128))
    zip_postal_code = db.Column(db.String(32))
    country = db.Column(db.String(64))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


db.create_all()
