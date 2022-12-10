from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import Form, SubmitField, StringField, IntegerField, TextAreaField, SelectField, PasswordField, \
    BooleanField, validators, DecimalField
from wtforms.validators import DataRequired
from datetime import datetime


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class SignUpForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Create Account')


class Addreceipt(Form):
    name = StringField('Name', [validators.DataRequired()])
    merchant = StringField('Merchant')
    dateOfPurchase = StringField('Date of Purchase (YYYY-MM-DD)', default = datetime.today().strftime('%Y-%m-%d'))
    returnDate = StringField('Return by date',)
    totalPrice = DecimalField('Price')
    numberOfItems = IntegerField('number of Items')
    description = TextAreaField("Description")
    image_1 = FileField('Receipt Image', validators=[ FileAllowed(['jpg', 'png'])])
