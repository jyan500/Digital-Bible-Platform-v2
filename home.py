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

	allBooks = getAllBooks(cur)

	## if user submits a form, send back response
	## TODO: turn the requesting chapters into ajax calls, so whenever user makes a selection in the book dropdown, the chapter dropdown
	## should update itself accordingly so user doesn't go out of bounds 
	if (request.method == "POST"):
		## if user has selected a book..
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

			print('book: ' , selectedBook, file = sys.stderr)
			print('chapter: ' ,selectedChapter, file = sys.stderr)

			## you have to pass the parameter values as a tuple for the execute statement
			## pass the chapter in for now
			selectedVerses = getVerseBodyRequest(selectedBook, selectedChapter)
			# resultValue = cur.execute("SELECT ESV, verse, id from esv where book = %s and chapter = %s", (selectedBook, selectedChapter))
			# if (resultValue > 0):
			# 	selectedVerses = cur.fetchall()
			# 	print(selectedChapter, file = sys.stderr)
			integerChapter = int(selectedChapter)
				## render the template with the saved attributes and with the verses
			return render_template("layout.html", bookOptions = allBooks, chapterOptions = getAllChaptersBook(cur, selectedBook), saveSelectedBook = selectedBook, saveSelectedChapter = integerChapter, selectedVerses = selectedVerses, is_bookmark = is_bookmark) 

	## for the AJAX request to get the chapters within each book			
	if request.method == "GET":
		## if user has only selected a book
		if (request.args.get('selectedbook') != None):
			selectedBook = request.args.get('selectedbook')
			print(selectedBook, file = sys.stderr)
			# resultValue = cur.execute("SELECT chapter from esv where book = %s group by chapter", (selectedBook, ))
			# if (resultValue > 0):
			# 	## save the selected chapters to avoid repeating the sql query
			# 	listForJson = []
			# 	for tup in cur.fetchall():
			# 		## append all the chapter names to the list
			# 		listForJson.append(tup[0])
			# 	session['chapterlistresult'] = listForJson
			return json.dumps({"chapterlist": getAllChaptersBook(cur, selectedBook)}) 

	return render_template("layout.html", bookOptions = allBooks)

@home_controller.route("/paginate", methods = ["GET"])
def paginate():
	if (request.method == "GET"):
		cur = mysql.connection.cursor()
		user_id = getUserID(cur, session.get('username'))
		selectedBook = request.args.get('selectedBook')
		selectedChapter = request.args.get('chapter')
		selectedVerses = getVerseBodyRequest(selectedBook, selectedChapter)
		is_bookmark = isExistingBookmark(cur, user_id, selectedBook, selectedChapter)
		print("selectedBook: " + selectedBook, file = sys.stderr)
		print("selectedChapter: " + str(selectedChapter), file = sys.stderr)
		# resultValue = cur.execute("SELECT ESV, verse, id from esv where book = %s and chapter = %s", (selectedBook, str(selectedChapter)))
		# if (resultValue > 0):
		# 	selectedVerses = cur.fetchall()
		print(selectedChapter, file = sys.stderr)
		integerChapter = int(selectedChapter)
		## render the template with the saved attributes and with the verses
		allBooks = getAllBooks(cur)
		allChaptersForBook = getAllChaptersBook(cur, selectedBook)
		return render_template("layout.html", bookOptions = allBooks , chapterOptions =  allChaptersForBook, saveSelectedBook = selectedBook, 
			saveSelectedChapter = integerChapter, selectedVerses = selectedVerses, is_bookmark = is_bookmark) 



