from unicodedata import category
from datetime import datetime
import secrets
from flask import render_template, redirect, url_for, request, flash, session, current_app
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash

from app import app as app

from app import db
from app import db
from app.forms import LoginForm
from app.models import User
import requests


@app.route('/', methods=['GET', 'POST'])
def index():
    return ('Lorem ipsum dolor sit amet')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Manges the login for customer trying to login
    Checks for the password and retieve the user profile for right user
    """
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('login'))
    return render_template('login.html', title='Sign In', form=form)
