from flask import render_template, request
from flask.helpers import flash, url_for
from werkzeug.utils import redirect

from . import landing
from ..models import Contact
from .forms import ContactForm
from .. import db

@landing.route('/', methods=['GET', 'POST'])
def landingpage():
    """
    Render the landingpage template on the / route
    """
    form = ContactForm()
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
    return render_template('landingpage/landingpage.html', form=form)

