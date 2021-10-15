from flask import render_template, abort
from flask_login import login_required, current_user

from . import landing

@landing.route('/')
def landingpage():
    """
    Render the landingpage template on the / route
    """
    return render_template('landingpage/landingpage.html')