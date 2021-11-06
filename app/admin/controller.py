"""
    Importing the needed modules to build the controllers function that will
    handle all the admin dashborad function/features.
"""
from flask import flash, redirect, render_template, url_for, jsonify, abort
from flask.globals import request
from flask_login import login_required, current_user
# Import the blueprint.
from . import admin
# Import the needed class forms.
from .forms import RegistrationForm
# Import the database variable.
from .. import db
# Import the RampAgent model.
from ..models import RampAgent, Flight

# Import more useful moduels.
import random


def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)


@admin.route('/', methods=['GET', 'POST'])
@login_required
def admin_dashboard():
    """
    prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)
    return render_template('admin/admin_dashboard.html')

@admin.route('/ramp_agent/all', methods=['GET', 'POST'])
def list_all_ramp_agents():
    """
    Handle requests to the /ramp_agent/all route
    List all the Ramp agents(employee).
    """
    check_admin()
    rampagents = RampAgent.query.all()
    print(rampagents)
    # Load all Ramp agents table page.
    return render_template('admin/rampagents/rampagents.html', rampagents=rampagents)


@admin.route('/ramp_agent/flights', methods=['GET', 'POST'])
def operated_flights():
    """
    Handle requests to the /ramp_agent/flights route
    List all the operated flights for all ramp agents.
    """
    flights = Flight.query.all()
    rampagentClass = RampAgent()
    # Load all flights table template page.
    return render_template('admin/operated_flights/list_all.html', flights=flights, rampagentClass=rampagentClass)



@admin.route('/ramp_agent/register', methods=['GET', 'POST'])
@login_required
def register_rampagent():
    """
    Handle requests to the /ramp_agent/register route
    Register a rampagent to the database through the registration form.
    """
    check_admin()
    register_rampagent = True
    # Create a form object from the registration form.
    form = RegistrationForm()
    if form.validate_on_submit():
        user_code = "TU" + str(random.randint(0000, 9999))
        rampagent = RampAgent(email=form.email.data,
                            first_name=form.first_name.data,
                            last_name=form.last_name.data,
                            password=user_code,
                            user_code=user_code)
        try:
            # add rampagent to the database
            db.session.add(rampagent)
            db.session.commit()
            flash('You have successfully registered new ramp agent.')
        except:
            # in case rampagent email already exists.
            flash('Error: Ramp agent email or User Code already exists.')

       # redirect to departments page
        return redirect(url_for('admin.list_all_ramp_agents'))
    return render_template('admin/rampagents/rampagent.html', form=form, register_rampagent=register_rampagent)

@admin.route('/ramp_agent/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_rampagent(id):
    """
    Handle requests to the /ramp_agent/edit/<int:id> route
    Edit a ramp agent's informations.
    """
    check_admin()
    register_rampagent = False
    # edit ramp agent with id!
    rampagent = RampAgent.query.get_or_404(id)
    form = RegistrationForm(obj=rampagent)
    if form.validate_on_submit():
        rampagent.first_name = form.first_name.data
        rampagent.last_name = form.last_name.data
        rampagent.email = form.email.data
        # Commit to the database.
        db.session.commit()
        flash('You have successfully edited the ramp agent informations.')

        # Redirect to the flights page
        return redirect(url_for('admin.list_all_ramp_agents'))
    form.first_name.data = rampagent.first_name
    form.last_name.data = rampagent.last_name
    form.email.data = rampagent.email
    # Load edit flight form template.
    return render_template('admin/rampagents/rampagent.html', form=form, register_rampagent=register_rampagent, rampagent=rampagent)

