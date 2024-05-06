from wtforms import (StringField,PasswordField,IntegerField,ValidationError, validators)
from flask_wtf import FlaskForm,Form
from flask_wtf.file import FileAllowed,FileField,FileRequired 
from .models import RegistrationDetails


class CustomerRegistrationForm(Form):
    full_name = StringField('Full Name',[validators.length(min=4, max=25),validators.DataRequired()])
    username = StringField('Username' ,[validators.length(min=4, max=25),validators.DataRequired()])
    email = StringField('Email',[validators.length(min=6, max=35),validators.Email(),validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired(),validators.EqualTo('confirm_password',message='Passwords must match')])
    confirm_password = PasswordField('Confirm Password',[validators.DataRequired()])
    age = IntegerField('Age',[validators.DataRequired()])
    contact = StringField('Contacts:', [validators.DataRequired()])

    profile = FileField('Profile', validators=[FileAllowed(['jpg','png','jpeg','gif'], 'Images only please')])


class CustomerLoginForm(Form):
    email = StringField('Email', [validators.Email(),validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])