"""
    Importing the needed modules to build the controllers function that will
    handle the authentication blueprint.
"""
from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user
# Import the blueprint
from . import auth
# Import the needed class forms.
from .forms import LoginForm
# Import the database variable.
from .. import db
# Import the RampAgent model.
from ..models import RampAgent

@auth.route('/admin_or_ramp_agent', methods=['GET', 'POST'])
def admin_or_ramp_agent():
    """
    Handle requests to the /admin_or_ramp_agent route
    Let the user choose to login as admin or as Ramp agnet.
    """
    return render_template('auth/admin_or_rampagent.html')


# @auth.route('/register', methods=['GET', 'POST'])
# def register():
#     """
#     Handle requests to the /register route
#     Add a rampagent to the database through the registration form.
#     """
#     # Create a form object from the registration form.
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         rampagent = RampAgent(email=form.email.data,
#                             first_name=form.first_name.data,
#                             last_name=form.last_name.data,
#                             password=form.password.data,
#                             user_code=form.user_code.data)
#         # add rampagent to the database
#         db.session.add(rampagent)
#         # Commit the changes
#         db.session.commit()
#         # Print a message to the user.
#         flash('You have successfully registered! You may now login.')
#         # redirect to the login page
#         return redirect(url_for('auth.login'))
#     return render_template('auth/register.html', form=form, title='Register')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle requests to the /login route
    Log an employee in through the login form
    """
    # Create a form object from the login form.
    form = LoginForm()
    if form.validate_on_submit():
        rampagent = RampAgent.query.filter_by(user_code=form.user_code.data).first()
        # Check whether rampagent exists in the database and whether
        # the password entered matches the password in the database.
        if rampagent is not None and rampagent.verify_password(form.password.data):
            # Log employee in.
            login_user(rampagent)
            # Redirect to the appropriate dashboard page.
            if rampagent.is_admin:
                return redirect(url_for('admin.admin_dashboard'))
            else:
                return redirect(url_for('dashboard.list_flights'))

        # When login details are incorrect, print messages to inform the user
        # about the situation!
        else:
            flash('Check your email or password.')
            flash('Check if you are you registered!')
    # Load login template.
    return render_template('auth/login.html',title='Login', form=form)


@auth.route('/logout')
@login_required
def logout():
    """
    Handle requests to the /logout route
    Log an employee out through the logout link
    """
    logout_user()
    flash('You have successfully been logged out.', 'info')
    # redirect to the landing page
    return redirect(url_for('landing.landingpage'))