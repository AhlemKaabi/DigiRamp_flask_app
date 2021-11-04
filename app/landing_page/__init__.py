from flask import Blueprint
# Creating the landing Blueprint
landing = Blueprint('landing', __name__)

from . import controller