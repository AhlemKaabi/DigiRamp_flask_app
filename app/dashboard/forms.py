from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

# from ..models import Flight
# start a flight form!
class FlightForm(FlaskForm):
    """
    Form for ramp agent to add a flight
    """
    flight_number = StringField(validators=[DataRequired()])
    departure = StringField(validators=[DataRequired()])
    destination = StringField(validators=[DataRequired()])
    aircraft_registration = StringField(validators=[DataRequired()])
    submit = SubmitField('Start Ramp Operations')

class UploadLoadsheet(FlaskForm):
    """
    add a loadshet Picture
    """
    flight_number = StringField('Flight number',validators=[DataRequired()])
    picture = FileField('Upload Loadsheet', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('add loadsheet')


class DisplayLoadsheet(FlaskForm):
    """
    display flight loadsheet
    """
    flight_number = StringField('Flight number',validators=[DataRequired()])
    submit = SubmitField('add loadsheet')
    
