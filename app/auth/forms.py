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
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(message='*Required'),
        EqualTo('password', message='Both password fields must be equal!')])

    submit = SubmitField('Register Account')
    # The users that create a new account should not have a used
    # email or email already registered in the database.
    def validate_email(self, field):
        if RampAgent.query.filter_by(email=field.data).first():
            raise ValidationError(message='Email is already in use.')


class LoginForm(FlaskForm):
    """
    Form for users to login.
    """
    email = StringField('Email')
    password = PasswordField('Password')
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Access Ramp Agent Dashboard')