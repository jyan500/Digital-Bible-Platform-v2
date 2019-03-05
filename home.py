from datetime import datetime 
from config import mysql, api_key
from extensions import *
home_controller = Blueprint('home_controller', __name__)

@home_controller.route("/", methods=['GET', 'POST'])
def index():
	## users should be prompted to login before going to the index page 
	if (not isUserLoggedIn()):
		return redirect(url_for('welcome_controller.landing_page'))
	cur = mysql.connection.cursor()
	user_id = getUserID(cur, session.get('username'))
	allBooks = getAllBooks(cur)
	## if user submits a form, send back response
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
			selectedVerses = getVerseBodyRequest(selectedBook, selectedChapter)
			integerChapter = int(selectedChapter)
			return render_template("layout.html", bookOptions = allBooks, chapterOptions = getAllChaptersBook(cur, selectedBook), saveSelectedBook = selectedBook, saveSelectedChapter = integerChapter, selectedVerses = selectedVerses, is_bookmark = is_bookmark) 

	## for the AJAX request to get the chapters within each book			
	if request.method == "GET":
		## if user has only selected a book
		if (request.args.get('selectedbook') != None):
			selectedBook = request.args.get('selectedbook')
			print(selectedBook, file = sys.stderr)
			return json.dumps({"chapterlist": getAllChaptersBook(cur, selectedBook)}) 

	return render_template("layout.html", bookOptions = allBooks)

@home_controller.route("/paginate", methods = ["GET"])
def paginate():
	print('------------ paginate -------------', file = sys.stderr)
	if (request.method == "GET"):
		cur = mysql.connection.cursor()
		user_id = getUserID(cur, session.get('username'))
		selectedBook = request.args.get('selectedBook')
		selectedChapter = request.args.get('chapter')
		selectedVerses = getVerseBodyRequest(selectedBook, selectedChapter)
		is_bookmark = isExistingBookmark(cur, user_id, selectedBook, selectedChapter)

		print("selectedBook: " + selectedBook, file = sys.stderr)
		print("selectedChapter: " + str(selectedChapter), file = sys.stderr)
		print(selectedChapter, file = sys.stderr)
		
		integerChapter = int(selectedChapter)
		allBooks = getAllBooks(cur)
		allChaptersForBook = getAllChaptersBook(cur, selectedBook)
		return render_template("layout.html", bookOptions = allBooks , chapterOptions =  allChaptersForBook, saveSelectedBook = selectedBook, 
			saveSelectedChapter = integerChapter, selectedVerses = selectedVerses, is_bookmark = is_bookmark) 



