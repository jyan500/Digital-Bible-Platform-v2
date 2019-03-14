from flask import Flask, render_template
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_wtf.csrf import CSRFError
from datetime import datetime
import os
from dotenv import load_dotenv
import sys
## configurations
# config = yaml.load(open('config.yaml'))

## load env file
load_dotenv(verbose = True)
app = Flask(__name__)

# app.config['MYSQL_HOST'] = config['mysql_host']
# app.config['MYSQL_USER'] = config['mysql_user']
# app.config['MYSQL_PASSWORD'] = config['mysql_password']
# app.config['MYSQL_DB'] = config['mysql_db']
# app.config['SECRET_KEY'] = config['secretkey']
# app.config['RECAPTCHA_PRIVATE'] = config['recaptcha_private']
# app.config['RECAPTCHA_PUBLIC'] = config['recaptcha_public']

app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['RECAPTCHA_PRIVATE'] = os.environ.get('RECAPTCHA_PRIVATE')
app.config['RECAPTCHA_PUBLIC'] = os.environ.get('RECAPTCHA_PUBLIC')

#### global variables ####
mysql = MySQL()

mysql.init_app(app)
recaptcha_private_key = app.config['RECAPTCHA_PRIVATE']
recaptcha_site_key = app.config['RECAPTCHA_PUBLIC']

## import our login page blueprint variable
from home import home_controller

## import our landing page blueprint
from welcome import welcome_controller

## import our login page blueprint variable
from login import login_controller

## import our signup page blueprint variable
from signup import signup_controller

## import our note_process_page 
from note_process_controller import note_process_controller

## import our logout page
from logout import logout_controller

## import our bookmarks page
from bookmarks import bookmarks_controller

## import our memory verse page
from memory_verse_controller import memory_verse_controller

from note_show_controller import note_show_controller

## register csrf protection
csrf = CSRFProtect(app)

## Register the home controller 
app.register_blueprint(home_controller)

## Register the landing page 
app.register_blueprint(welcome_controller)

## Register the login controller ## 
app.register_blueprint(login_controller)

## Register the logout controller ##
app.register_blueprint(logout_controller)

## Register the signup controller ##
app.register_blueprint(signup_controller)

## Register the note_process controller
app.register_blueprint(note_process_controller)

## Register the bookmarks controller
app.register_blueprint(bookmarks_controller)

## Register the memory verse controller
app.register_blueprint(memory_verse_controller)

## Register the note show controller
app.register_blueprint(note_show_controller)


@app.errorhandler(404)
# function which takes error as parameter
def not_found(error):
	return render_template("404.html")

@app.context_processor
def utility_processor():

    def date_now(format="%d.m.%Y %H:%M:%S"):
        return datetime.now().strftime(format)

    def name():
        return "BibleJourney"

    return dict(date_now=date_now, company=name)

@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    return render_template('404.html')