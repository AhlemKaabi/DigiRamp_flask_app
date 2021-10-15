from flask import flash, redirect, render_template, url_for, request
from flask_login import login_required, login_user, logout_user

from . import auth
from .forms import LoginForm, RegistrationForm
from .. import db
from ..models import RampAgent

@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle requests to the /register route
    Add a rampagent to the database through the registration form
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        rampagent = RampAgent(email=form.email.data,
                            first_name=form.first_name.data,
                            last_name=form.last_name.data,
                            password=form.password.data)
        # add rampagent to the database
        db.session.add(rampagent)
        db.session.commit()
        flash('You have successfully registered! You may now login.')
        # redirect to the login page
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form, title='Register')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle requests to the /login route
    Log an employee in through the login form
    """
    form = LoginForm()
    if form.validate_on_submit():
        # check whether rampagent exists in the database and whether
        # the password entered matches the password in the database
        rampagent = RampAgent.query.filter_by(email=form.email.data).first()
        if rampagent is not None and rampagent.verify_password(form.password.data):
            # log employee in
            login_user(rampagent)
            # redirect to the appropriate dashboard page --> function inthe controller dashboard that enter the propper template
            return redirect(url_for('dashboard.list_flights'))
        # when login details are incorrect
        else:
            flash('Check your email or password.')
            flash('Check if you are you registered!')
    # load login template
    return render_template('auth/login.html',title='Login', form=form)
    # return redirect(url_for('dashboard.list_flights'))


@auth.route('/logout')
@login_required
def logout():
    """
    Handle requests to the /logout route
    Log an employee out through the logout link
    """
    logout_user()
    flash('You have successfully been logged out.', 'info')
    # redirect to the login page
    return redirect(url_for('auth.login'))