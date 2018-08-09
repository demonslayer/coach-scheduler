from flaskr.db import get_db
from werkzeug.security import generate_password_hash

def user_exists(username):
	return get_db().execute(
		'SELECT id FROM user where username = ?', (username,)
	).fetchone() is not None

def create_user(username, password, coach_id):
	db = get_db()
	db.execute(
		'INSERT INTO user (username, password, coach_id) VALUES (?,?,?)',
		(username, generate_password_hash(password), coach_id)
	)
	db.commit()

def fetch_user_by_name(username):
	return get_db().execute(
		'SELECT * FROM user WHERE username = ?', (username,)
	).fetchone()

def fetch_user_by_id(user_id):
	return get_db().execute(
			'SELECT * FROM user WHERE id =?', (user_id,)
	).fetchone()