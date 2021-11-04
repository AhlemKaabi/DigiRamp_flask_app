"""
    Importing the needed modules to build the controllers function that will
    handle the landing page blueprint.
"""
from flask import render_template, request
from flask.helpers import flash, url_for
from werkzeug.utils import redirect
# Import the blueprint.
from . import landing
# Import the Contact models.
from ..models import Contact
# Import the needed class forms.
from .forms import ContactForm
# Import the database variable.
from .. import db

@landing.route('/', methods=['GET', 'POST'])
def landingpage():
    """
    Handle requests to the / route
    """
    form = ContactForm()
    # contact form.
    if request.method == 'POST':
        if form.validate_on_submit():
            message = Contact(first_name=form.first_name.data,
                                last_name=form.last_name.data,
                                email=form.email.data,
                                message=form.message.data)
            # add message to the database
            db.session.add(message)
            db.session.commit()
            flash('Your message was sent successfully!')
            return redirect(url_for('landing.landingpage'))
    # Load the landing page template.
    return render_template('landingpage/landingpage.html', form=form)

