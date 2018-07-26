from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from flask import Blueprint
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import sys

## import our own mysql extension
from extensions import mysql

signup = Blueprint('signup', __name__)

@signup.route("/signup", methods = ["GET", "POST"])
def signuppage():
	
	if (request.method == "POST"):
		username = request.form['username']
		password = request.form['password']
		password_conf = request.form['password_conf']
		if not (username and password and password_conf):
			flash("Username or Password cannot be empty.")
			return redirect(url_for('signup.signuppage'))
		if (password != password_conf):
			flash("The passwords that were typed did not match, please try again.")
			return redirect(url_for('signup.signuppage'))
		else:
			username = username.strip()
			password = password.strip()
		# returns salted pwd hash in format: method$salt$hashedvalue
		hashedPassword = generate_password_hash(password, 'sha256')
		cur = mysql.connection.cursor()
		resultValue = cur.execute("SELECT username from USERS where username = %s", (username, ))
		## if a user with the username already exists
		if (resultValue > 0):
			flash("Sorry, username already exists.")
			return redirect(url_for('signup.signuppage'))
		else:
			## insert the new user 
			print("Username: " + username +  "hashpassword: " + hashedPassword, file = sys.stderr)
			cur.execute("INSERT INTO USERS (USERNAME, PASSWORD_HASH) VALUES ( %s, %s )", (username, hashedPassword))
			mysql.connection.commit()
			flash("User account has been created. Please login")	
			return redirect(url_for('login.loginpage'))
	return render_template("signup.html")




