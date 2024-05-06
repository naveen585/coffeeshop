from flask_wtf import Form
from wtforms import (StringField,PasswordField,SubmitField,FloatField,DateTimeField,SelectField,TextField,TextAreaField,IntegerField, validators)

class SignUpForm(Form):
    full_name = StringField('Full Name',[validators.length(min=4, max=25)])
    username = StringField('Username' ,[validators.length(min=4, max=25)])
    email = StringField('Email',[validators.length(min=6, max=35),validators.Email()])
    password = PasswordField('Password', [validators.DataRequired(),validators.EqualTo('confirm_password',message='Passwords must match')])
    confirm_password = PasswordField('Confirm Password')
    age = IntegerField('Age')


class SignInForm(Form):
    email = StringField('Email', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])