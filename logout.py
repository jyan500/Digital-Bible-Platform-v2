## own files
from config import mysql
from extensions import * 

logout_controller = Blueprint('logout', __name__)

@logout_controller.route("/logout", methods = ["GET", "POST"])
def logoutpage():
	user = session.get('username')
	session.clear()
	if (user != None):
		flash(user + " has logged out successfully!", 'Success')
	return redirect(url_for('login.loginpage'))
