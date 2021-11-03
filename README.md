# <p align="center">DigiRamp flask application </p>

## Table of Content :mag_right:

- [Introduction](#Introduction)
- [Environment](#Environment)
- [Installation](#Installation)
- [Technologies](#Technologies)
- [Usage](#Usage)
- [License](#License)

# Introduction :page_with_curl:

<img src="img/blog.png">

DigiRamp is a web application written in flask micro-framework. It is a solution for airline companies that offers leaner communication across multiple departments while preparing the aircraft for the next flight.

To use a demo of the app click [here](http://46.101.79.78/)
### Disclaimer :exclamation:
do not use any real information(emails-password on the demo)!! the app is still in development and lacks security testing.
### Authors :pencil2:
Ahlem kaabi
[linked-in](https://www.linkedin.com/in/k-ahlem/)

# Environment

This project is interpreted/tested on Ubuntu 20.04 LTS using python3 (version 3.8.10) and MySql ( Ver 8.0.26-0ubuntu0.20.04.2 )

# Installation :floppy_disk:
This guide will help you to start using the web application in your local environment

### Requirements:

	- Python >= 3.8.10
	- pip
	- MySql ( Ver 8.0.26-0ubuntu0.20.04.2 )

### Steps:
#### Setup the database:
1. create a database `Your_db_Name`
	```
	CREATE DATABASE Your_db_Name;
	```
2. create a user `User_Name` with password `Your_password`
	```
	CREATE USER 'User_Name'@'localhost' IDENTIFIED BY 'Your_password';
	```
3. for `User_Name` grant all privileges on the `Your_db_Name` database
	```
	GRANT ALL PRIVILEGES ON Your_db_Name . * TO 'User_Name'@'localhost';
	```
#### Get the code base
1. clone the repository on your computer
2. pip install -r requirements.txt
3. inside the project directory create instance/config.py file
> We will put configuration variables here
that will not be pushed to version control
due to their sensitive nature.
In this case, we put the secret key
as well as the database URI which contains the database.
```
# instance/config.py

SECRET_KEY = '<^>YOUR_SECRET_KEY^>'
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://User_Name:Your_password@localhost/Your_db_Name'
```
4. run these commands:
```
$ flask db init
$ flask db migrate
$ flask db upgrade
```
5. final step
```
$ export FLASK_CONFIG=development
$ export FLASK_APP=run.py
$ flask run
```

<img src="img/readme_pic.png">

# Technologies :computer:
<img src="img/Digiramp.png">

# Usage :steam_locomotive:

## Add New flight
<img src="img/add_flight.png">

## Supervise a flight turnaround processes:
<img src="img/supervise.png">

## Upload and display required informations:
<img src="img/upload_.png">

<img src="img/display_.png">

## Display data tables - Operated flight:
<img src="img/tableoperated.png">

## Display airports IATA Codes:
<img src="img/iata.png">
# License :lock:


This project is licensed under the MIT License see [MIT LICENSE](https://github.com/AhlemKaabi/DigiRamp_flask_app/blob/main/LICENSE) file for more details
### Final word :black_nib:

This project was written as part of the curriculum for Holberton School. Holberton School's methodology uses project-based learning and peer-learning to teach students the theory and tools needed to adapt to the future and ever-changing technologies. For more information, visit [this link](https://www.holbertonschool.com/).