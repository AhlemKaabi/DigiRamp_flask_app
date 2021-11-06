from flask import Blueprint
# Creating the admin Blueprint
admin = Blueprint('admin', __name__)

from . import controller