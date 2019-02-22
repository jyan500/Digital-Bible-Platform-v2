from flask_mysqldb import MySQL
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
import json
import sys

mysql = MySQL()

def isUserLoggedIn():
	## users should be prompted to login before going to the index page 
	return session.get('username') != None

def getUserID(cur: 'mysql', username: str):
	resultValue = cur.execute('SELECT uid FROM users WHERE username = %s', (username,))
	if (resultValue > 0):
		id = cur.fetchall()[0][0]
		print(id, file = sys.stderr)
		return id
	## return -1 if the username somehow doesn't match with the userid
	else:
		return -1

def handleBookmarks(cur: 'mysql', user_id: int, book: str, chapter: int, start_verse: int = 0, end_verse: int = 0, is_memory_verse: bool = False):
	if (is_memory_verse):
		query = "INSERT INTO bookmarks (user_id, book, chapter, start_verse, end_verse, is_memory_verse) VALUES (%s, %s, %s, %s, %s, %s)"
		cur.execute(query, (str(user_id), book, str(chapter), str(start_verse), str(end_verse), str(1)))
	else:
		query = "INSERT INTO bookmarks (user_id, book, chapter) VALUES (%s, %s, %s)"
		cur.execute(query, (str(user_id), book, str(chapter)))
	mysql.connection.commit()


