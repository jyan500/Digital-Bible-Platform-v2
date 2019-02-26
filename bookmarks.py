from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from flask import Blueprint
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import sys
import json 
import extensions
from extensions import mysql 

bookmarks = Blueprint('bookmarks', __name__)

@bookmarks.route("/bookmarks", methods=['GET', 'POST'])
def bookmarks_page():
	## users should be prompted to login before going to the index page 
	if (not extensions.isUserLoggedIn()):
		return redirect(url_for('login.loginpage'))


	cur = mysql.connection.cursor()
	user_id = extensions.getUserID(cur, str(session['username']))
	bookmarks_list = getUserBookMarks(cur, user_id)

	if request.method == 'GET':
		## get the user's bookmarks
		return render_template('bookmarks.html', bookmark_list = bookmarks_list)
	elif request.method == 'POST':
		return json.dumps({'finished': 1})

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

def deleteUserBookmark(cur, user_id, bookmark_id):
	pass

		
