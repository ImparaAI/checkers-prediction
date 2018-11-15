import MySQLdb
from flask import current_app, g

def get_connection(connect_to_database = True):
	if 'db' in g:
		return g.db

	db = MySQLdb.connect(host = 'mysql', db = 'prediction') if connect_to_database else MySQLdb.connect(host = 'mysql')
	db.autocommit(True)

	if connect_to_database:
		g.db = db

	return db

def get_cursor():
	return get_connection().cursor()

def execute(sql, args = None):
	cursor = get_cursor()
	cursor.execute(sql, args)
	cursor.close()

def fetchone(sql, args = None):
	cursor = get_cursor()
	cursor.execute(sql, args)
	result = cursor.fetchone()
	cursor.close()

	return result

def fetchall(sql, args = None):
	cursor = get_cursor()
	cursor.execute(sql, args)
	result = cursor.fetchall()
	cursor.close()

	return result

def close_database(e = None):
	db = g.pop('db', None)

	if db is not None:
		db.close()

def initialize():
	db = get_connection(connect_to_database = False)

	if database_already_initialized():
		return False

	with current_app.open_resource('database/schema.sql') as f:
		cursor = db.cursor()
		cursor.execute(f.read().decode('utf8'))
		cursor.close()

	return True

def database_already_initialized():
	cursor = get_connection(connect_to_database = False).cursor()
	cursor.execute("SHOW DATABASES LIKE 'prediction'")

	return not not cursor.fetchone()