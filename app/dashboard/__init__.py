from flask import Blueprint
# Creating the dashboard Blueprint
dashboard = Blueprint('dashboard', __name__)

from . import controller