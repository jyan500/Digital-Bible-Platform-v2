from datetime import datetime 
from config import api_key, mysql
from extensions import *
home_controller = Blueprint('home_controller', __name__)

@home_controller.route("/", methods=['GET', 'POST'])
def index():
	## users should be prompted to login before going to the index page 
	if (not isUserLoggedIn()):
		return redirect(url_for('login.loginpage'))
	cur = mysql.connection.cursor()
	user_id = getUserID(cur, session.get('username'))

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
		is_bookmark = False
		if (request.form.get('booklist') != None and request.form.get('chapterlist') != None):

			selectedBook = request.form['booklist']
			## the selectedChapter needs to be a string for the resultvalue, but passed in as an integer to the form
			selectedChapter = request.form['chapterlist']
			is_bookmark = isExistingBookmark(cur, user_id, selectedBook, selectedChapter)
			if (request.form.get('bookmark')):
				ifBookmark = request.form['bookmark']
				if (ifBookmark == '1'):
					handleBookmarks(mysql.connection, user_id, selectedBook, selectedChapter)
					flash("Bookmarked Successfully!", "Success")
					is_bookmark = True 

			print(selectedBook, file = sys.stderr)

			## you have to pass the parameter values as a tuple for the execute statement
			## pass the chapter in for now
			resultValue = cur.execute("SELECT ESV, verse, id from esv where book = %s and chapter = %s", (selectedBook, selectedChapter))
			if (resultValue > 0):
				selectedVerses = cur.fetchall()
				print(selectedChapter, file = sys.stderr)
				integerChapter = int(selectedChapter)
				## render the template with the saved attributes and with the verses
				return render_template("layout.html", bookOptions = session['booklistresult'], chapterOptions = session['chapterlistresult'], saveSelectedBook = selectedBook, saveSelectedChapter = integerChapter, selectedVerses = selectedVerses, is_bookmark = is_bookmark) 

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

@home_controller.route("/paginate", methods = ["GET"])
def paginate():
	if (request.method == "GET"):
		cur = mysql.connection.cursor()
		user_id = getUserID(cur, session.get('username'))
		selectedBook = request.args.get('selectedBook')
		selectedChapter = request.args.get('chapter')
		is_bookmark = isExistingBookmark(cur, user_id, selectedBook, selectedChapter)
		print("selectedBook: " + selectedBook, file = sys.stderr)
		print("selectedChapter: " + str(selectedChapter), file = sys.stderr)
		resultValue = cur.execute("SELECT ESV, verse, id from esv where book = %s and chapter = %s", (selectedBook, str(selectedChapter)))
		if (resultValue > 0):
			selectedVerses = cur.fetchall()
			print(selectedChapter, file = sys.stderr)
			integerChapter = int(selectedChapter)
			## render the template with the saved attributes and with the verses
			if (session.get('booklistresult') == None):
				session['booklistresult'] = getAllBooks(cur)
			if (session.get('chapterlistresult') == None):
				session['chapterlistresult'] = getAllChaptersBook(cur, selectedBook)
			return render_template("layout.html", bookOptions = session['booklistresult'] , chapterOptions =  session['chapterlistresult'], saveSelectedBook = selectedBook, 
				saveSelectedChapter = integerChapter, selectedVerses = selectedVerses, is_bookmark = is_bookmark) 



