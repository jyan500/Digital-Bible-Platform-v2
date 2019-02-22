from flask import Flask, flash, redirect, render_template, request, session, abort, jsonify, url_for
from flask_mysqldb import MySQL
from flask import Blueprint
import time
from datetime import datetime
import bleach
import sys
import json


## yaml reads in serialized information as a key-value pair
import yaml

## import our own mysql shared variable 
from extensions import mysql

note_process_controller = Blueprint('note_process_controller', __name__)

@note_process_controller.route("/note_insert", methods = ["POST"])
def insert():
	## users should be prompted to login before going to the index page 
	if (not extensions.isUserLoggedIn()):
		return redirect(url_for('login.loginpage'))

	if (request.method == "POST"):
		## create notes table
		## take the text from the popover
		note_content = request.form['note-content']
		verse_id = request.form['verse-id']
		print(verse_id, file = sys.stderr)
		## sanitize the text
		bleach.clean(note_content)
		## print(note_content, file=sys.stderr)
		bleach.clean(verse_id)

		ts = time.time()
		timestamp = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

		cur = mysql.connection.cursor()
		## get the uid of the user who is logged on
		print(session['username'], file = sys.stderr)
		resultValue = cur.execute("SELECT uid FROM users WHERE username = %s", (session['username'], ))
		uid = 0
		if resultValue > 0:
			uid = cur.fetchall()[0][0]
			print(uid, file = sys.stderr)

		## insert into database
		if (uid != 0):
			print(note_content, file = sys.stderr)
			cur.execute("INSERT INTO note (verse_id, note_content, date, uid) VALUES (%s, %s, %s, %s)", (verse_id, note_content, timestamp, uid))
			mysql.connection.commit()
			##flash("Note saved successfully!", "Success")
			return json.dumps({'status':'OK'});
		else:
			##flash("You must be a registered user to save notes!", "Error")
			return json.dumps({'status':'Error'});

@note_process_controller.route("/note_show", methods=["GET"])
def show():
	## users should be prompted to login before going to the index page 
	if (not extensions.isUserLoggedIn()):
		return redirect(url_for('login.loginpage'))

	if (request.method == "GET"):
		## show Notes 
		## take the text from the popover
		if (request.args.get('verse-id') != None):
			verse_id = request.args.get('verse-id')
			print("verseid in show: " + verse_id, file = sys.stderr)

			cur = mysql.connection.cursor()
			## get the uid of the user who is logged on
			print(session['username'], file = sys.stderr)
			resultValue = cur.execute("SELECT uid FROM users WHERE username = %s", (session['username'], ))
			uid = 0
			if resultValue > 0:
				uid = cur.fetchall()[0][0]
				print(uid, file = sys.stderr)

			## select from database
			if (uid != 0):
				resultValue = cur.execute("SELECT note_content FROM note WHERE note.verse_id = %s AND note.uid = %s", (verse_id, uid))
				##flash("Note saved successfully!", "Success")
				if (resultValue > 0):
					note = cur.fetchall()[0][0]	
					print('note: '  + note, file = sys.stderr)
					return json.dumps({'note_content': note })
				else:
					return json.dumps({'note_content': ""})

		else:
			##flash("You must be a registered user to save notes!", "Error")
			return json.dumps({'status':'Error'})

@note_process_controller.route("/note_update", methods=["POST"])
def update():
	## users should be prompted to login before going to the index page 
	if (not extensions.isUserLoggedIn()):
		return redirect(url_for('login.loginpage'))
		
	if (request.method == "POST"):
		## create notes table
		## take the text from the popover
		note_content = request.form['note-content']
		verse_id = request.form['verse-id']
		print(verse_id, file = sys.stderr)
		## sanitize the text
		bleach.clean(note_content)
		## print(note_content, file=sys.stderr)
		bleach.clean(verse_id)

		ts = time.time()
		timestamp = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

		cur = mysql.connection.cursor()
		## get the uid of the user who is logged on
		print(session['username'], file = sys.stderr)
		resultValue = cur.execute("SELECT uid FROM users WHERE username = %s", (session['username'], ))
		uid = 0
		if resultValue > 0:
			uid = cur.fetchall()[0][0]
			print(uid, file = sys.stderr)

		## check to see if there's an existing note
		resultValue = cur.execute("SELECT id FROM note WHERE uid = %s AND verse_id = %s", (uid, verse_id, ))
		existingNoteID = 0
		if (resultValue > 0):
			print("existing Note Id: " + str(cur.fetchall()[0][0]), file = sys.stderr)

		## insert into database
		if (uid != 0 and resultValue > 0):
			print("note_content: " + note_content, file = sys.stderr)
			cur.execute("UPDATE note set note_content = %s, date = NOW() where verse_id = %s AND uid = %s", (note_content, verse_id, uid))
			mysql.connection.commit()
			##flash("Note saved successfully!", "Success")
			return json.dumps({'status':'OK'});
		else:
			##flash("You must be a registered user to save notes!", "Error")
			return json.dumps({'status':'Error'});

