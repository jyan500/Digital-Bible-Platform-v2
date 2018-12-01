from flask_mysqldb import MySQL
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
import json
import sys

mysql = MySQL()

def getUserID(cur: 'mysql', username: str):
	resultValue = cur.execute('SELECT uid FROM users WHERE username = %s', (username,))
	if (resultValue > 0):
		id = cur.fetchall()[0][0]
		print(id, file = sys.stderr)
		return id
	## return -1 if the username somehow doesn't match with the userid
	else:
		return -1


