from flask import Flask, flash, redirect, render_template, request, session, abort, jsonify
from flask import Blueprint
from flask_mysqldb import MySQL
import sys

login = Blueprint('login', __name__)

@login.route("/login")
def loginpage():
	return render_template("login.html") 


