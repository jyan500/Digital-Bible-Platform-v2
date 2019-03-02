## only in this file so far
import re
## own files
from config import api_key, mysql
from extensions import * 

memory_verse_controller = Blueprint('memory_verse_controller', __name__)

@memory_verse_controller.route("/memory_verse", methods = ["GET", "POST"])
def memory_verse_page():

	## users should be prompted to login before going to the index page 
	if (not isUserLoggedIn()):
		return redirect(url_for('login.loginpage'))
	## establish connection with mysql
	cur = mysql.connection.cursor()	
	user_id = getUserID(cur, str(session['username']))

	too_many_verses = ''' We are sorry, as can only provide flashcards with a maximum of 10 verses at a time.
							Please save multiple flashcards to break the verses into smaller chunks '''
	if (request.method == "GET"):
		assoc = getSavedMemoryVerses(cur, user_id)		
		return render_template('memory_verse.html', memory_dict = assoc)
	if (request.method == "POST"):
		## regex format: James 1:2-2
		regex = re.compile('^([a-zA-Z]+)(\\s\\d+)([:]?\\d+)?([-]?\\d+)?$')
		verse = request.form.get('verse-input')
		print(request.form, file = sys.stderr)
		print('Within post method', file = sys.stderr)
		if (verse != None):
			match = regex.match(verse)
			if (match):
				match_groups = match.groups()
				print('Match found: ', match.groups(), len(match.groups()), file = sys.stderr)

				book = match_groups[0]
				chapter = match_groups[1].strip()
				param_list = [book, chapter]
				start_verse = match_groups[2]
				end_verse = match_groups[3]


				if (start_verse != None and end_verse != None):
					start_verse = start_verse.replace(':','')
					end_verse = end_verse.replace('-', '')
					difference = int(end_verse) - int(start_verse);
					print("Difference: " , difference, file = sys.stderr)
					if (difference > 10):
						flash(too_many_verses, 'Error')
						return redirect(url_for('memory_verse_controller.memory_verse_page'));
					print('Params: ', book, chapter, start_verse, end_verse, file = sys.stderr)
				elif(start_verse != None):
					start_verse = start_verse.replace(':','')
					end_verse = 0
				else:
					flash(too_many_verses, 'Error')
					return redirect(url_for('memory_verse_controller.memory_verse_page'));

				## handle bookmarks 	
				verseBody = getVerseBodyRequest(book, chapter, str(start_verse), str(end_verse))
				if (verseBody):		
					if (request.form.get('save-verse')):
						print('is bookmark', file =sys.stderr)
						is_bookmark_request = request.form['save-verse']
						if (is_bookmark_request == '1'):
							is_memory_verse = True;
							selectedVerse = handleBookmarks(mysql.connection, user_id, book, chapter, start_verse, end_verse, is_memory_verse)
							flash("Saved " + verse + " Successfully!", 'Success')
							return render_template('memory_verse.html', saved_verse = verse, selected_verses = verseBody, is_bookmark = is_memory_verse)
						else:
							flash("Oops something went wrong! Please Try Again", 'Error')
							return redirect(url_for('memory_verse_controller.memory_verse_page'))

					is_bookmark = isExistingBookmark(cur, user_id, book, chapter, start_verse, end_verse, True)	
					return render_template('memory_verse.html', saved_verse = verse, selected_verses = verseBody, is_bookmark = is_bookmark)
				else:
					flash("Oops! We were not able to find " + verse + ", please try again", 'Error')
					return redirect(url_for('memory_verse_controller.memory_verse_page'))
			else:
				# if no regex match
				flash("Please enter like so: James 1:2, James 1:2-3", 'Error')
				return redirect(url_for('memory_verse_controller.memory_verse_page'))


@memory_verse_controller.route("/saved_memory_verse", methods = ["GET"])
def get_existing_memory_verse():

	print('--------------- get_existing_memory_verse --------------', file = sys.stderr)
	## users should be prompted to login before going to the index page 
	if (not isUserLoggedIn()):
		return redirect(url_for('login.loginpage'))
		
	cur = mysql.connection.cursor()
	user_id = getUserID(cur, str(session['username']))

	book = request.args.get('book')
	chapter = request.args.get('chapter')
	start_verse = request.args.get('start_verse')
	end_verse = request.args.get('end_verse')
	print('start_verse: ', start_verse, 'end_verse: ' , end_verse, file =sys.stderr)
	verse_body = getVerseBodyRequest(book, chapter, str(start_verse), str(end_verse))
	is_bookmark = isExistingBookmark(cur, user_id, book, chapter, start_verse, end_verse, True)
	saved_verse = ''
	print('end_verse in saved_memory_verse: ' , end_verse, file = sys.stderr)	
	if (end_verse == '0'):
		saved_verse = "{} {}:{}".format(book, chapter, start_verse, end_verse)
	else:
		saved_verse = "{} {}:{}-{}".format(book, chapter, start_verse, end_verse)

	print('saved_verse: ' , saved_verse, file = sys.stderr)
	return render_template('memory_verse.html', saved_verse = saved_verse, selected_verses = verse_body, is_bookmark=is_bookmark)
		
@memory_verse_controller.route("/memory_verse_post", methods = ["POST"])
def memoryVerseDelete():
	## users should be prompted to login before going to the index page 
	if (not isUserLoggedIn()):
		return redirect(url_for('login.loginpage'))

	cur = mysql.connection.cursor()
	user_id = getUserID(cur, str(session['username']))

	if (request.method == "POST"):
		memory_verse_id = request.form.get('id-to-submit')
		print("memory_verse_id: ", memory_verse_id, file = sys.stderr)
		if (memory_verse_id != None and memory_verse_id.isdigit()):
			query = "DELETE FROM bookmarks WHERE bookmarks.id = %s AND bookmarks.user_id = %s"	
			print('delete memory_verse query: ' , query, file = sys.stderr)
			result_value = cur.execute(query, (memory_verse_id, user_id))
			mysql.connection.commit()
			if (result_value > 0):
				flash("Deleted Successfully", "Success")
			else:
				flash("Failed to delete", "Error")
	return redirect(url_for('memory_verse_controller.memory_verse_page'))

def getSavedMemoryVerses(cur: 'mysql', user_id: int ):
	query = 'SELECT id, book, chapter, start_verse, end_verse FROM bookmarks WHERE user_id = %s AND is_memory_verse = 1'
	resultValue = cur.execute(query, (user_id, ))
	assoc = []
	if (resultValue > 0):
		selectedMemoryVerses = cur.fetchall()
		print(selectedMemoryVerses, file = sys.stderr)
		for i in range(len(selectedMemoryVerses)):
			verses_dict = dict()
			print('creating the ', i, ' assoc', file = sys.stderr)
			verses_dict['id'] = selectedMemoryVerses[i][0]
			verses_dict['book'] = selectedMemoryVerses[i][1]
			verses_dict['chapter'] = selectedMemoryVerses[i][2]	
			verses_dict['start_verse'] = selectedMemoryVerses[i][3]
			verses_dict['end_verse'] = selectedMemoryVerses[i][4]
			assoc.append(verses_dict)

	print(assoc, file = sys.stderr)
	return assoc




















