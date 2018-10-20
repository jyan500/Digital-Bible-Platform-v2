from flask import Flask, flash, redirect, render_template, request, session, abort, jsonify
from flask_mysqldb import MySQL
import sys
import json

## yaml reads in serialized information as a key-value pair
import yaml

## import our own mysql shared variable 
from extensions import mysql

## import our login page blueprint variable
from login import login

## import our signup page blueprint variable
from signup import signup

## import our note_process_page 
from note_process_controller import note_process_controller

## import our logout page
from logout import logout


## configurations
config = yaml.load(open('config.yaml'))
app = Flask(__name__)

app.config['MYSQL_HOST'] = config['mysql_host']
app.config['MYSQL_USER'] = config['mysql_user']
app.config['MYSQL_PASSWORD'] = config['mysql_password']
app.config['MYSQL_DB'] = config['mysql_db']
app.config['SECRET_KEY'] = config['secretkey']

mysql.init_app(app)

## Register the login controller ## 
app.register_blueprint(login)

## Register the logout controller ##
app.register_blueprint(logout)
## Register the signup controller ##
app.register_blueprint(signup)

## Register the note_process controller
app.register_blueprint(note_process_controller)

@app.route("/", methods=['GET', 'POST'])
def index():
	## user should be able to view the index page without being logged in, but extra features will be available to the user 
	## if they login
	if not session.get('username'):
		flash("Welcome! Please login to make full use of the website's features.")
	cur = mysql.connection.cursor()
	## always populate the dropdown with available chapters in the Bible, then save it in session variable
	if (session.get('booklistresult') == None):
		## resultValue is an integer 
		resultValue = cur.execute("SELECT book from esv group by book order by id")
		if (resultValue > 0):
			## booklistresult is a list of tuples
			session['booklistresult'] = cur.fetchall()
			print(session['booklistresult'], file = sys.stderr)

	## if user submits a form, send back response
	## TODO: turn the requesting chapters into ajax calls, so whenever user makes a selection in the book dropdown, the chapter dropdown
	## should update itself accordingly so user doesn't go out of bounds 
	if (request.method == "POST"):
		## if user has selected a book..
		## if user has selected a book and chapter, 
		if (request.form.get('booklist') != None and request.form.get('chapterlist') != None):
			selectedBook = request.form['booklist']
			## the selectedChapter needs to be a string for the resultvalue, but passed in as an integer to the form
			selectedChapter = request.form['chapterlist']
			print(selectedBook, file = sys.stderr)
			## you have to pass the parameter values as a tuple for the execute statement
			## pass the chapter in for now
			resultValue = cur.execute("SELECT ESV, verse, id from esv where book = %s and chapter = %s", (selectedBook, selectedChapter))
			if (resultValue > 0):
				selectedVerses = cur.fetchall()
				print(selectedChapter, file = sys.stderr)
				integerChapter = int(selectedChapter)
				## render the template with the saved attributes and with the verses
				return render_template("layout.html", bookOptions = session['booklistresult'], chapterOptions = session['chapterlistresult'], saveSelectedBook = selectedBook, saveSelectedChapter = integerChapter, selectedVerses = selectedVerses) 

	## for the AJAX request to get the chapters within each book			
	if request.method == "GET":
		## if user has only selected a book
		if (request.args.get('selectedbook') != None):
			selectedBook = request.args.get('selectedbook')
			print(selectedBook, file = sys.stderr)
			resultValue = cur.execute("SELECT chapter from esv where book = %s group by chapter", (selectedBook, ))
			if (resultValue > 0):
				## save the selected chapters to avoid repeating the sql query
				listForJson = []
				for tup in cur.fetchall():
					## append all the chapter names to the list
					listForJson.append(tup[0])
				session['chapterlistresult'] = listForJson
				return json.dumps({"chapterlist": listForJson}) 

	return render_template("layout.html", bookOptions = session['booklistresult'])


if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0', port=5000)



