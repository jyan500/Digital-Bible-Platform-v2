#### global imports ####

## import our mysql connection and api key
from flask import Flask, flash, redirect, render_template, request, session, abort, jsonify, url_for
from flask import Blueprint
import json
import requests
import re
import sys

#### global functions ####

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

def handleBookmarks(connection: 'mysql.connection', user_id: int, book: str, chapter: int, start_verse: int = 0, end_verse: int = 0, is_memory_verse: bool = False):
	query = "INSERT INTO bookmarks (user_id, book, chapter, start_verse, end_verse, is_memory_verse) VALUES (%s, %s, %s, %s, %s, %s)"
	if (is_memory_verse):
		connection.cursor().execute(query, (str(user_id), book, str(chapter), str(start_verse), str(end_verse), str(1)))
	else:
		connection.cursor().execute(query, (str(user_id), book, str(chapter), str(start_verse), str(end_verse), str(0)))
	connection.commit()

def isExistingBookmark(cur: 'mysql', user_id: int, book: str, chapter: int, start_verse: int = 0, end_verse: int = 0, is_memory_verse: bool = False):
	query = 'SELECT count(*) as cnt FROM bookmarks WHERE user_id = %s AND book = %s AND chapter = %s AND start_verse = %s AND end_verse = %s AND is_memory_verse = %s'
	print('is_memory_verse: ', is_memory_verse, file = sys.stderr)
	resultValue = cur.execute(query, (user_id, book, chapter, start_verse, end_verse, is_memory_verse))
	if (resultValue > 0):
		count = cur.fetchall()
		print('count: ', count[0][0], file = sys.stderr)
		return count[0][0] == 1
	return False

## get all chapters for one book 
def getAllChaptersBook(cur: 'mysql', book: str):
	## get the last chapter
	query = 'SELECT num_chapters FROM book_ref WHERE book = %s'
	result_value = cur.execute(query, (book,))
	if (result_value > 0):
		# for tup in cur.fetchall():
		# 	## append all the chapter names to the list
		# 	listForJson.append(tup[0])
		num_chapters = cur.fetchall()[0][0]
		return [i for i in range(1, num_chapters+1)]

## get all books in the bible
def getAllBooks(cur: 'mysql'):

	query = 'SELECT book FROM book_ref ORDER BY id'
	result_value = cur.execute(query)
	if (result_value > 0):
		results_tuple = cur.fetchall()
		return results_tuple
		return [results_tuple[i] for i in range(len(results_tuple))]

## get verse body (Currently not in use)
# def getVerseBody(cur: 'mysql', book: str, chapter: int, start_verse: int = 0, end_verse: int = 0):
# 	rangeQuery = ''
# 	query = 'SELECT ESV, verse, id from esv WHERE book = %s AND chapter = %s'
# 	param_list = [book, chapter]
# 	assoc = []
# 	if (start_verse != 0 and end_verse != 0):
# 		range_query = ' AND verse BETWEEN %s AND %s'
# 		param_list.append(start_verse)
# 		param_list.append(end_verse)
# 	elif (start_verse != 0):
# 		range_query = ' AND verse = %s'
# 		param_list.append(start_verse)

# 	if (range_query != ''):
# 		query += range_query

# 	resultValue = cur.execute(query, tuple(param_list))
# 	if (resultValue > 0):
# 		selectedVerse = cur.fetchall()
# 		print(selectedVerse, file = sys.stderr)
# 		for i in range(len(selectedVerse)):
# 			verses_dict = dict()
# 			verses_dict['body'] = selectedVerse[i][0]
# 			verses_dict['verse_num'] = selectedVerse[i][1]
# 			verses_dict['verse_id'] = selectedVerse[i][2]
# 			assoc.append(verses_dict)
# 	return assoc 


## version is world english bible by default until different versions are supported
def getVerseBodyRequest(book: str, chapter: str, start_verse: str = '0', end_verse: str = '0', version: str = 'web'):
	## if start verse and end verse are provided
	## world english bible api id: 9879dbb7cfe39e4d-01
	API_URL = 'https://getbible.net/json?passage='
	sanitize_chapter = chapter.strip()
	sanitize_book = book.strip()
	sanitize_start_verse = start_verse.strip()
	sanitize_end_verse = end_verse.strip()
	print('book: ' , sanitize_book, 'chapter: ' , sanitize_chapter, 'start_verse: ', sanitize_start_verse, 'end_verse: ', sanitize_end_verse, file = sys.stderr)
	if (start_verse != '0' and end_verse != '0'):
		query_string = '{} {}:{}-{}'.format(sanitize_book, sanitize_chapter, sanitize_start_verse, sanitize_end_verse)	
	## if just start verse
	elif (start_verse != '0'):
		query_string = '{} {}:{}'.format(sanitize_book, sanitize_chapter, sanitize_start_verse)	
	else:
		query_string = '{} {}'.format(sanitize_book, sanitize_chapter)
	
	API_URL = 'https://getbible.net/json?passage={}&version={}'.format(query_string, version)
	print(API_URL, file =sys.stderr)
	response = requests.get(API_URL)
	## trim the outer parenthesis to convert from jsonp to json
	data = response.text.split("(", 1)[1].strip(");")
	json_data = json.loads(data)
	## json response for the api changes depending on whether th e 
	# print(json_data, file = sys.stderr)
	if (start_verse != '0'):
		## current response: { book: [] }
		outer_list = json_data['book']
		chapter_data = outer_list[0]['chapter']
	else:
		chapter_data = json_data['chapter']
	# print(chapter_data, file =sys.stderr)
	verses_dict_list = []
	for verses_key in chapter_data:
		verses_dict = dict()
		verses_dict['book'] = sanitize_book
		verses_dict['chapter'] = sanitize_chapter
		verses_dict['verse'] = verses_key
		verses_dict['text'] = chapter_data[verses_key]['verse']
		verses_dict_list.append(verses_dict)
	return verses_dict_list
	# print(response.json(), file = sys.stderr)
	## convert from jsonp to json
	# try:
	# 	return passages['verses']
	# except:
	# 	return passages['error'] 

def getExistingNotes(cur: 'mysql', user_id: int, book_filter: str = '', chapter_filter: int = 0):
	condition = ''
	params = [user_id] 
	if (book_filter != ''):
		condition += ' AND book_filter = %s '
		params.append(book_filter)
	if (chapter_filter != 0):
		condition += ' AND chapter_filter = %s '
		params.append(chapter_filter)
	query = "SELECT note_content, date, book, chapter, verse FROM note WHERE uid = %s"
	query += condition
	result_value = cur.execute(query, tuple(params))
	resultsAssocList = []
	if (result_value > 0):
		results = cur.fetchall()
		for i in range(len(results)):
			resultsAssoc = dict()
			resultsAssoc['note_content'] = results[i][0]
			resultsAssoc['date'] = results[i][1]
			resultsAssoc['book'] = results[i][2]
			resultsAssoc['chapter'] = results[i][3]
			resultsAssoc['verse'] = results[i][4]
			resultsAssocList.append(resultsAssoc)
	return resultsAssocList



