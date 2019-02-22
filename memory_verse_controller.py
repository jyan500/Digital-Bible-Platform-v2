from flask import Flask, flash, redirect, render_template, request, session, abort, jsonify, url_for
from flask_mysqldb import MySQL
import sys
import json

## only in this file so far
import re

from flask import Blueprint


## own files
import extensions
from extensions import mysql 

memory_verse_controller = Blueprint('memory_verse_controller', __name__)

@memory_verse_controller.route("/memory_verse", methods = ["GET", "POST"])
def memory_verse_page():

	## users should be prompted to login before going to the index page 
	if (not extensions.isUserLoggedIn()):
		return redirect(url_for('login.loginpage'))
	## establish connection with mysql
	cur = mysql.connection.cursor()	
	user_id = extensions.getUserID(cur, str(session['username']))

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
				if (request.form.get('save-verse')):
					print('is bookmark', file =sys.stderr)
					is_bookmark = request.form['save-verse']
					if (is_bookmark == '1'):
						
						is_memory_verse = True;
						selectedVerse = extensions.handleBookmarks(cur, user_id, book, chapter, start_verse, end_verse, is_memory_verse)
						flash("Saved " + verse + " Successfully!", 'Success')
						return render_template('memory_verse.html', saved_verse = verse, selected_verses = selectedVerse)
					else:
						flash("Oops something went wrong! Please Try Again", 'Error')
						return redirect(url_for('memory_verse_controller.memory_verse_page'))
				is_bookmark = extensions.isExistingBookmark(cur, user_id, book, chapter, start_verse, end_verse, True)	
				verseBody = getVerseBody(cur, book, chapter, start_verse, end_verse)	
				if (verseBody):
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

	## users should be prompted to login before going to the index page 
	if (not extensions.isUserLoggedIn()):
		return redirect(url_for('login.loginpage'))
		
	cur = mysql.connection.cursor()
	user_id = extensions.getUserID(cur, str(session['username']))

	book = request.args.get('book')
	chapter = request.args.get('chapter')
	start_verse = request.args.get('start_verse')
	end_verse = request.args.get('end_verse')

	verse_body = getVerseBody(cur, book, int(chapter), int(start_verse), int(end_verse))
	is_bookmark = extensions.isExistingBookmark(cur, user_id, book, chapter, start_verse, end_verse)
	saved_verse = ''
	print('end_verse in saved_memory_verse: ' , end_verse, file = sys.stderr)	
	if (end_verse == '0'):
		saved_verse = "{} {}:{}".format(book, chapter, start_verse, end_verse)
	else:
		saved_verse = "{} {}:{}-{}".format(book, chapter, start_verse, end_verse)

	print('saved_verse: ' , saved_verse, file = sys.stderr)
	return render_template('memory_verse.html', saved_verse = saved_verse, selected_verses = verse_body, is_bookmark=is_bookmark)
		


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

def getVerseBody(cur: 'mysql', book: str, chapter: int, start_verse: int = 0, end_verse: int = 0):
	rangeQuery = ''
	query = 'SELECT ESV, verse, id from esv WHERE book = %s AND chapter = %s'
	param_list = [book, chapter]
	assoc = []
	if (start_verse != 0 and end_verse != 0):
		range_query = ' AND verse BETWEEN %s AND %s'
		param_list.append(start_verse)
		param_list.append(end_verse)
	elif (start_verse != 0):
		range_query = ' AND verse = %s'
		param_list.append(start_verse)

	if (range_query != ''):
		query += range_query

	resultValue = cur.execute(query, tuple(param_list))
	if (resultValue > 0):
		selectedVerse = cur.fetchall()
		print(selectedVerse, file = sys.stderr)
		for i in range(len(selectedVerse)):
			verses_dict = dict()
			verses_dict['body'] = selectedVerse[i][0]
			verses_dict['verse_num'] = selectedVerse[i][1]
			verses_dict['verse_id'] = selectedVerse[i][2]
			assoc.append(verses_dict)
	return assoc 


















