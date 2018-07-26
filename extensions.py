from flask_mysqldb import MySQL
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
import json

mysql = MySQL()

