import MySQLdb
from flask import current_app, g

def get_database():
	if 'db' not in g:
		g.db = MySQLdb.connect(host = 'mysql')

	return g.db

def close_database(e = None):
	db = g.pop('db', None)

	if db is not None:
		db.close()

def initialize():
	db = get_database()

	if database_already_initialized():
		return False

	with current_app.open_resource('database/schema.sql') as f:
		cursor = db.cursor()
		cursor.execute(f.read().decode('utf8'))
		cursor.close()

	return True

def database_already_initialized():
	cursor = get_database().cursor()
	cursor.execute("SHOW DATABASES LIKE 'prediction'")

	return not not cursor.fetchone()