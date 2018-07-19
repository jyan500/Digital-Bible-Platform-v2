from flask import Flask, flash, redirect, render_template, request, session, abort, jsonify
from flask import Blueprint
from flask_mysqldb import MySQL
import sys

signup = Blueprint('signup', __name__)

@signup.route("/signup")
def loginpage():
	return "this is our signup page"

