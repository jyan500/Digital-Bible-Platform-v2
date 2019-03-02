import time
from datetime import datetime
import bleach
from config import mysql
from extensions import *

note_process_controller = Blueprint('note_process_controller', __name__)

@note_process_controller.route("/note_insert", methods = ["POST"])
def insert():
	## users should be prompted to login before going to the index page 
	if (not isUserLoggedIn()):
		return redirect(url_for('login.loginpage'))

	if (request.method == "POST"):
		## create notes table
		## take the text from the popover
		note_content = request.form['note-content']
		verse = request.form['verse']
		chapter = request.form['chapter']
		book = request.form['book']

		## sanitize the text
		bleach.clean(note_content)
		print(note_content, file=sys.stderr)
		bleach.clean(verse)

		ts = time.time()
		timestamp = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

		cur = mysql.connection.cursor()
		## get the uid of the user who is logged on
		print(session['username'], file = sys.stderr)
		uid = getUserID(cur, session['username']) 
		## insert into database
		if (uid != 0):
			print(note_content, file = sys.stderr)
			cur.execute("INSERT INTO note (verse, chapter, book,  note_content, date, uid) VALUES (%s, %s, %s, %s, %s, %s)", (str(verse), chapter, book, note_content, timestamp, uid))
			mysql.connection.commit()
			##flash("Note saved successfully!", "Success")
			return json.dumps({'status':'OK'});
		else:
			##flash("You must be a registered user to save notes!", "Error")
			return json.dumps({'status':'Error'});

@note_process_controller.route("/note_show", methods=["GET"])
def show():
	## users should be prompted to login before going to the index page 
	if (not isUserLoggedIn()):
		return redirect(url_for('login.loginpage'))

	if (request.method == "GET"):
		## show Notes 
		## take the text from the popover
		if (request.args.get('verse') != None):
			# verse_id = request.args.get('verse-id')
			verse = request.args.get('verse')
			chapter = request.args.get('chapter')
			book = request.args.get('book')
			cur = mysql.connection.cursor()
			## get the uid of the user who is logged on
			uid = getUserID(cur, session['username'])
			print('verse: ', verse, 'chapter: ', chapter, 'book: ', book)
			## select from database
			if (uid != 0):
				## resultValue = cur.execute("SELECT note_content FROM note WHERE note.verse_id = %s AND note.uid = %s", (verse_id, uid))
				query = "SELECT note_content FROM note WHERE note.verse = %s AND note.uid = %s AND note.book = %s AND note.chapter = %s"
				resultValue = cur.execute(query, (verse, uid, book, chapter))
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
	if (not isUserLoggedIn()):
		return redirect(url_for('login.loginpage'))
		
	if (request.method == "POST"):
		## create notes table
		## take the text from the popover
		note_content = request.form['note-content']
		verse = request.form['verse']
		chapter = request.form['chapter']
		book = request.form['book']
		## sanitize the text
		bleach.clean(note_content)
		## print(note_content, file=sys.stderr)
		bleach.clean(verse)

		ts = time.time()
		timestamp = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

		cur = mysql.connection.cursor()
		## get the uid of the user who is logged on
		uid = getUserID(cur, session['username'])
		## check to see if there's an existing note
		resultValue = cur.execute("SELECT id FROM note WHERE uid = %s AND verse = %s AND chapter = %s AND book = %s", (uid, verse, chapter, book ))
		existingNoteID = 0
		if (resultValue > 0):
			# print("existing Note Id: " + str(cur.fetchall()[0][0]), file = sys.stderr)
			existingNoteID = cur.fetchall()[0][0]
			print('existingNoteID: ', str(existingNoteID))

		## insert into database
		if (uid != 0 and resultValue > 0):
			print("note_content: " + note_content, file = sys.stderr)
			cur.execute("UPDATE note set note_content = %s, date = NOW() where id = %s AND uid = %s", (note_content, existingNoteID, uid))
			mysql.connection.commit()
			##flash("Note saved successfully!", "Success")
			return json.dumps({'status':'OK'});
		else:
			##flash("You must be a registered user to save notes!", "Error")
			return json.dumps({'status':'Error'});

