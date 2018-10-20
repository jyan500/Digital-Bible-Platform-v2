from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from flask import Blueprint
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import sys

## own files
from extensions import mysql 

logout = Blueprint('logout', __name__)

@logout.route("/logout", methods = ["GET", "POST"])

def logoutpage():
	user = session.get('username')
	session.clear()
	if (user != None):
		flash(user + " has logged out successfully!", 'Success')
	return redirect(url_for('login.loginpage'))
