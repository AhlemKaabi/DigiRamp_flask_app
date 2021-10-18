#----------------------------------------------------------------------------#

# third-party imports
from flask import Flask, render_template
# pip install flask-login #
from flask_login import LoginManager
# pip install flask-migrate #
from flask_migrate import Migrate

from flask_sqlalchemy import SQLAlchemy

from flask_caching import Cache

#----------------------------------------------------------------------------#

# local imports
from config import app_config

#----------------------------------------------------------------------------#
cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})

# db variable initialization
db = SQLAlchemy()
# To use Flask-Login, we need to create a LoginManager object and initialize it
login_agent = LoginManager()


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    cache.init_app(app)

    # Bootstrap(app)
    db.init_app(app)

    # initializing the LoginManager object
    login_agent.init_app(app)
    #if a user tries to access a page that they are not
    # authorized to, it will redirect to the specified view
    # and display the specified message.
    login_agent.login_message = "You must be logged in to access this page."
    login_agent.login_view = "auth.login"



    # migrate object which will allow us to run migrations using Flask-Migrate
    migrate = Migrate(app, db)

    from app import models

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .dashboard import dashboard as dashboard_blueprint
    app.register_blueprint(dashboard_blueprint, url_prefix='/dashboard')


    from .landing_page import landing as landing_blueprint
    app.register_blueprint(landing_blueprint)

    @app.errorhandler(403)
    def forbidden(error):
        return render_template('errors/403.html', title='Forbidden'), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('errors/404.html', title='Page Not Found'), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template('errors/500.html', title='Server Error'), 500

    # @app.route('/500')
    # def error():
    #     abort(500)


    return app