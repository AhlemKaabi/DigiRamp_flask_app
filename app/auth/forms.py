from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo

from ..models import RampAgent

class RegistrationForm(FlaskForm):
    """
    Form for users to create new account
    """
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(message='*Required'),
        EqualTo('password', message='Both password fields must be equal!')])

    submit = SubmitField('Register Account')

    def validate_email(self, field):
        if RampAgent.query.filter_by(email=field.data).first():
            raise ValidationError(message='Email is already in use.')


class LoginForm(FlaskForm):
    """
    Form for users to login
    """
    # email = StringField('Email', validators=[DataRequired(), Email()])
    # password = PasswordField('Password', validators=[DataRequired()])
    # remember_me = BooleanField('Remember Me')
    # submit = SubmitField('Access Ramp Agent Dashboard')

    email = StringField('Email')
    password = PasswordField('Password')
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Access Ramp Agent Dashboard')