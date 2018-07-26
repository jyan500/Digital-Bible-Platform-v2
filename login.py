from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from flask import Blueprint
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import sys

## own files
from extensions import mysql 

login = Blueprint('login', __name__)

@login.route("/login", methods = ["GET", "POST"])
def loginpage():
	if (request.method == "POST"):
		username = request.form['username']
		password = request.form['password']
		if not (username and password):
			flash("Username or Password cannot be empty.")
			return redirect(url_for('login'))
		else:
			username = username.strip()
			password = password.strip()

		cur = mysql.connection.cursor()
		## check if user exists
		resultValue1 = cur.execute("SELECT USERNAME, PASSWORD_HASH from USERS where USERNAME = %s", (username, ))
		if (resultValue1 > 0):
			userAndPassTuple = cur.fetchall()[0]
			db_password = userAndPassTuple[1]
			## if the plaintext password matches a password hash of the user 
			if (check_password_hash(db_password, password)):
				flash("Welcome " + username + "!")
				## store the username as a key, and value as boolean
				session["username"] = True
				return redirect(url_for("index"))
			else:
				flash("Invalid Username or Password")
	return render_template("login.html") 


