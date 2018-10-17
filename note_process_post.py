from flask import Flask, flash, redirect, render_template, request, session, abort, jsonify
from flask_mysqldb import MySQL
from flask import Blueprint
import bleach
import sys
import json

## yaml reads in serialized information as a key-value pair
import yaml

## import our own mysql shared variable 
from extensions import mysql

note_process_post = Blueprint('note_process_post', __name__)

@note_process_post.route("/note_process_post", methods = ["POST"])
def process():
	if (request.method == "POST"):
		## create notes table
		## take the text from the popover
		note_content = request.form['note_section']
		## sanitize the text
		bleach.clean(note_content)
		## print(note_content, file=sys.stderr)
		## insert into database
		return note_content


