"""
    Importing the needed modules to build the forms classes that will
    handle diffrent forms.
"""
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class FlightForm(FlaskForm):
    """
    Form for ramp agent to add a flight.
    """
    flight_number = StringField(validators=[DataRequired()])
    departure = StringField(validators=[DataRequired()])
    destination = StringField(validators=[DataRequired()])
    aircraft_registration = StringField(validators=[DataRequired()])
    submit = SubmitField('Start Ramp Operations')

class UploadLoadsheet(FlaskForm):
    """
    Upload a loadshet picture form.
    """
    flight_number = StringField('Flight number',validators=[DataRequired()])
    picture = FileField('Upload Loadsheet', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('add loadsheet')


class DisplayLoadsheet(FlaskForm):
    """
    Display a loadshet picture form.
    """
    flight_number = StringField('Flight number',validators=[DataRequired()])
    submit = SubmitField('Display loadsheet')
