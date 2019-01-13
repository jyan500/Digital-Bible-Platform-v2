from flask import Flask, flash, redirect, render_template, request, session, abort, jsonify, url_for
from flask_mysqldb import MySQL
import sys
import json
from flask import Blueprint

## own files
from extensions import mysql 

memory_verse_controller = Blueprint('memory_verse_controller', __name__)

@memory_verse_controller.route("/memory_verse", methods = ["GET", "POST"])
def memory_verse():
	if (request.method == "GET"):
		return render_template('memory_verse.html')
