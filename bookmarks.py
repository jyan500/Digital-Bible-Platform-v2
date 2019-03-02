from extensions import * 
from config import mysql
bookmarks_controller = Blueprint('bookmarks', __name__)

@bookmarks_controller.route("/bookmarks", methods=['GET', 'POST'])
def bookmarks_page():
	## users should be prompted to login before going to the index page 
	if (not isUserLoggedIn()):
		return redirect(url_for('login.loginpage'))
	cur = mysql.connection.cursor()
	user_id = getUserID(cur, str(session['username']))
	bookmarks_list = getUserBookMarks(cur, user_id)

	if request.method == 'GET':
		## get the user's bookmarks
		return render_template('bookmarks.html', bookmark_list = bookmarks_list)

@bookmarks_controller.route("/bookmarks_post", methods = ['POST'])
def deleteUserBookmark():
	if (not isUserLoggedIn()):
		return redirect(url_for('login.loginpage'))

	cur = mysql.connection.cursor()
	user_id = getUserID(cur, str(session['username']))

	if request.method == 'POST':
		bookmark_id = request.form.get('id-to-submit')
		if (bookmark_id != None and bookmark_id.isdigit()):
			print('bookmark_id: ' , bookmark_id, file =sys.stderr)
			query = "DELETE FROM bookmarks WHERE bookmarks.user_id = %s AND bookmarks.id = %s"
			result_value = cur.execute(query, (user_id, bookmark_id))
			mysql.connection.commit()
			if (result_value > 0):
				flash("Deleted successfully", "Success")
			else:
				flash("Error, failed to delete.", "Error")
	return redirect(url_for('bookmarks.bookmarks_page'))


def getUserBookMarks(cur, user_id: int):
	result = cur.execute("SELECT * FROM bookmarks where user_id = %s AND is_memory_verse != 1", (str(user_id), ))
	bookmarks_dict_list = [] 
	if (result > 0):
		bookmarks_tuple = cur.fetchall()
		for i in range(len(bookmarks_tuple)):
			bookmarks_dict = dict()
			bookmarks_dict['bookmark_id'] = bookmarks_tuple[i][0]
			bookmarks_dict['user_id'] = bookmarks_tuple[i][1]
			bookmarks_dict['book'] = bookmarks_tuple[i][2]
			bookmarks_dict['chapter'] = bookmarks_tuple[i][3]
			bookmarks_dict_list.append(bookmarks_dict)
	return bookmarks_dict_list


		
