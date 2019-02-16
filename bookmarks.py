from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from flask import Blueprint
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import sys

import extensions
from extensions import mysql 

bookmarks = Blueprint('bookmarks', __name__)

@bookmarks.route("/bookmarks", methods=['GET', 'POST'])
def bookmarks_page():
	## get the user's bookmarks
	cur = mysql.connection.cursor()
	bookmarks_list = getUserBookMarks(cur, extensions.getUserID(cur, session['username']) )
	return render_template('bookmarks.html', bookmark_list = bookmarks_list)

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

		
