from flask import render_template, request, flash
from flask_login import login_required, current_user

from . import landing
from ..models import Contact
from .forms import ContactForm
from .. import db

@landing.route('/', methods=['GET', 'POST'])
def landingpage():
    """
    Render the landingpage template on the / route
    """
    if request.method == 'POST':
        form = ContactForm()
        if form.validate_on_submit():
            message = Contact(first_name=form.first_name.data,
                                last_name=form.last_name.data,
                                email=form.email.data,
                                message=form.message.data)
            # add message to the database
            db.session.add(message)
            db.session.commit()
            flash('your message was sent successfully!')
    return render_template('landingpage/landingpage.html', form=form)

