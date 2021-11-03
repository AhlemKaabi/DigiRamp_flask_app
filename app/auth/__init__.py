from flask import Blueprint
# Creating the authentication Blueprint
auth = Blueprint('auth', __name__)

from . import controller