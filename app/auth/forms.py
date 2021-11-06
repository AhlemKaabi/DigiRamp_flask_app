"""
    Importing the needed modules to build the forms classes that will
    handle the registration and the login of an employee.
"""
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo

# class RegistrationForm(FlaskForm):
#     """
#     Form for users to create new account.
#     """
#     first_name = StringField('First Name', validators=[DataRequired()])
#     last_name = StringField('Last Name', validators=[DataRequired()])
#     email = StringField('Email', validators=[DataRequired(), Email()])
#     password = PasswordField('Password', validators=[DataRequired()])
#     confirm_password = PasswordField('Confirm Password', validators=[DataRequired(message='*Required'),
#         EqualTo('password', message='Both password fields must be equal!')])
#     user_code = StringField('user_code', validators=[DataRequired()])
#     submit = SubmitField('Register Account')
#     # The users that create a new account should not have a used
#     # email or email already registered in the database.
#     def validate_email(self, field):
#         if RampAgent.query.filter_by(email=field.data).first():
#             raise ValidationError(message='Email is already in use.')

#     def validate_code(self, field):
#         if RampAgent.query.filter_by(code=field.data).first():
#             raise ValidationError('Username is already in use.')

class LoginForm(FlaskForm):
    """
    Form for users to login.
    """
    user_code = StringField('Code', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Access Dashboard')