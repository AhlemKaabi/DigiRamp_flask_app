"""
    Importing the needed modules to build the forms classes that will
    handle the registration and the login of an employee.
"""
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo
# Import the RampAgent model
from ..models import RampAgent

class RegistrationForm(FlaskForm):
    """
    Form for users to create new account.
    """
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Register Account')
