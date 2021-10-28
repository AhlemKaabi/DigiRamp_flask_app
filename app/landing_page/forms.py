from flask_wtf import FlaskForm
from wtforms import  TextAreaField, StringField, SubmitField
from wtforms.validators import DataRequired, Email

from ..models import RampAgent

class ContactForm(FlaskForm):
    """
    Form for users to create new account
    """
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    message = TextAreaField('Text', render_kw={"rows": 70, "cols": 11}, validators=[DataRequired()])
    submit = SubmitField('Submit Message')
