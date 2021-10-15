# an instance directory
# a config.py file:
# We will put configuration variables here
# that will not be pushed to version control
# due to their sensitive nature.
# In this case, we put the secret key
# as well as the database URI which contains the database
# user password.
SECRET_KEY = '<^>YOUR_SECRET_KEY^>'
SQLALCHEMY_DATABASE_URI = 'mysql://db_admin:dt2021@localhost/perform_better_db'