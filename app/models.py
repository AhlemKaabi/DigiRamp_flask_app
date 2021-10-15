
# a model is a representation of a database table in code.
# my database tables:
# RampAgent
# Flight
# contact
# processes_data

import app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
# generate_password_hash, which allows us to hash passwords
# check_password_hash, which allows us to ensure the hashed password matches the password
from app import db, login_agent

class RampAgent(UserMixin, db.Model):
    """
    Create an RampAgent table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'rampagents'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        """
        Prevent password from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<RampAgent: {} {}>'.format(self.first_name, self.last_name)

# Set up user_loader
# user_loader callback, which Flask-Login uses
# to reload the user object from the user ID stored in the session
@login_agent.user_loader
def load_user(user_id):
    return RampAgent.query.get(int(user_id))


class Flight(db.Model):
    """
    Create a Flight table
    """
    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'flights'

    id = db.Column(db.Integer, primary_key=True)
    flight_number = db.Column(db.String(20), index=True, unique=True)
    departure = db.Column(db.String(20), index=True)
    destination = db.Column(db.String(20), index=True)
    aircraft_registration = db.Column(db.String(20), index=True)
    rampagent_id = db.Column(db.Integer, db.ForeignKey('rampagents.id'))


    def __repr__(self):
        return '<Flight: {}>'.format(self.flight_number)


class Process(db.Model):
    """
    Create a Process table
    """
    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'processes'

    id = db.Column(db.Integer, primary_key=True)
    process_name = db.Column(db.String(60), index=True,)
    start_time = db.Column(db.String(60), index=True)
    end_time = db.Column(db.String(60), index=True)
    status = db.Column(db.String(60), index=True)
    flight_id = db.Column(db.Integer, db.ForeignKey('flights.id'))
    rampagent_id = db.Column(db.Integer, db.ForeignKey('rampagents.id'))

#     def __repr__(self):
#         return '<Process: {}>'.format(self.process_name)
# #######################
# 	# backref allows us to create a new property on the RampAgent model
# 	# such that we can use ' rampagent.flight ' or ' rampagent.process '
# # 	# to get the flight or process assigned to that rampagent
# # ######################