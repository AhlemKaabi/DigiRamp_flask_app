from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms import SelectField
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
