from datetime import datetime 
from config import mysql, api_key
from extensions import *
welcome_controller = Blueprint('welcome_controller', __name__)

@welcome_controller.route("/home", methods = ["GET"])
def landing_page():
	if (isUserLoggedIn()):
		return redirect(url_for('home.index'))	
	else:
		return render_template('welcome.html')
		
@welcome_controller.route("/about", methods = ["GET"])
def about_page():
	if (isUserLoggedIn()):
		return redirect(url_for('home.index'))
	else:
		return render_template('about.html')
