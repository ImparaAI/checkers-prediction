import flask
import sqlite3
from datetime import datetime

def get_connection():
	if 'db_connection' not in flask.g:
		connection = sqlite3.connect(flask.current_app.config['DATABASE_FILE'], detect_types = sqlite3.PARSE_DECLTYPES)
		connection.isolation_level = None #autocommit

		flask.g.db_connection = connection

	return flask.g.db_connection

def get_cursor():
	return get_connection().cursor()

def execute(sql, args = ()):
	cursor = get_cursor()
	cursor.execute(sql, args)
	cursor.close()

def insert(sql, args = ()):
	cursor = get_cursor()
	cursor.execute(sql, args)

	id = cursor.lastrowid
	cursor.close()

	return id

def fetchone(sql, args = ()):
	cursor = get_cursor()
	cursor.execute(sql, args)
	result = cursor.fetchone()
	cursor.close()

	return result

def fetchall(sql, args = ()):
	cursor = get_cursor()
	cursor.execute(sql, args)
	result = cursor.fetchall()
	cursor.close()

	return result

def close_database(e = None):
	connection = flask.g.pop('db_connection', None)

	if connection is not None:
		connection.close()

def initialize():
	if database_already_initialized():
		return False

	with flask.current_app.open_resource('database/schema.sql') as f:
		cursor = get_cursor()
		cursor.executescript(f.read().decode('utf8'))
		cursor.close()

	return True

def database_already_initialized():
	cursor = get_cursor()
	cursor.execute("SELECT count(*) FROM sqlite_master WHERE type = 'table' AND name != 'android_metadata' AND name != 'sqlite_sequence';")

	return cursor.fetchone()[0] > 1

def get_current_time():
	return datetime.now().strftime('%Y-%m-%d %H:%M:%S')