from flask import Flask, flash, redirect, render_template, request, session, abort, jsonify, url_for
from flask_mysqldb import MySQL
import sys
import json

## only in this file so far
import re

from flask import Blueprint


## own files
from extensions import mysql 

memory_verse_controller = Blueprint('memory_verse_controller', __name__)

@memory_verse_controller.route("/memory_verse", methods = ["GET", "POST"])
def memory_verse_page():
	if (request.method == "POST"):
		## regex format: James 1:2-2
		regex = re.compile('^([a-zA-Z]+)(\\s\\d+)([:]?\\d+)?([-]?\\d+)?$')
		verse = request.form.get('verse-input')
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


				range_query = ''
				if (start_verse != None and end_verse != None):
					start_verse = start_verse.replace(':','')
					end_verse = end_verse.replace('-', '')
					difference = int(end_verse) - int(start_verse);
					print("Difference: " , difference, file = sys.stderr)
					# if (difference > 4):
					# 	flash('''We are very sorry, as can only provide flashcards with a maximum of 4 verses at a time.
					# 		Please save multiple flashcards to break the verses into smaller chunks ''', 'Error')
					# 	return redirect(url_for('memory_verse_controller.memory_verse_page'));
					range_query = ' AND verse BETWEEN %s AND %s'
					param_list.append(start_verse)
					param_list.append(end_verse)

					print('Params: ', book, chapter, start_verse, end_verse, file = sys.stderr)
				elif(start_verse != None):
					start_verse = start_verse.replace(':','')
					range_query = ' AND verse = %s';
					param_list.append(start_verse);
					print('Params: ' , book, chapter, start_verse, file = sys.stderr)

				## establish connection with mysql
				cur = mysql.connection.cursor()
				query = 'SELECT ESV, verse, id from esv WHERE book = %s AND chapter = %s'

				if (range_query != ''):
					query += range_query

				resultValue = cur.execute(query, tuple(param_list))
				if (resultValue > 0):
					selectedVerse = cur.fetchall()
					return render_template('memory_verse.html', saved_verse = verse, selected_verses = selectedVerse)
				else:
					flash("Oops! We were not able to find " + verse + ", please try again", 'Error')
					return redirect(url_for('memory_verse_controller.memory_verse_page'))
			else:
				# if no regex match
				flash("Please enter like so: James 1:2-3, James 1, James 1:2", 'Error')
				return redirect(url_for('memory_verse_controller.memory_verse_page'))
	return render_template('memory_verse.html')





