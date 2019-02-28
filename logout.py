## own files
from extensions import * 

logout = Blueprint('logout', __name__)

@logout.route("/logout", methods = ["GET", "POST"])

def logoutpage():
	user = session.get('username')
	session.clear()
	if (user != None):
		flash(user + " has logged out successfully!", 'Success')
	return redirect(url_for('login.loginpage'))
