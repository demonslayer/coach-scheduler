import functools

from flask import (
	Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
	db = get_db()
	all_coaches = db.execute('SELECT * FROM coach').fetchall()

	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		coach_id = request.form['coach']

		error = None

		coach = db.execute( 'SELECT * FROM coach WHERE id = ?', (coach_id,)).fetchone()

		if not username:
			error = 'You need a username'
		elif not password:
			error = 'You need a password'
		elif not coach_id or not coach:
			error = 'You need a coach'
		elif db.execute(
			'SELECT id FROM user where username = ?', (username,)
		).fetchone() is not None:
			error = 'username {} is taken'.format(username)

		if error is None:
			db.execute(
				'INSERT INTO user (username, password, coach_id) VALUES (?,?,?)',
				(username, generate_password_hash(password), coach_id)
			)
			db.commit()
			return redirect(url_for('auth.login'))

		flash (error)

	return render_template('auth/register.html', coaches = all_coaches)

@bp.route('/login', methods=('GET', 'POST'))
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']

		print("YOU ARE HERE")

		db = get_db()
		error = None
		user = db.execute(
			'SELECT * FROM user WHERE username = ?', (username,)
		).fetchone()

		print("YOU ARE AFTER DB")

		if user is None:
			error = 'Incorrect Username'
		elif not check_password_hash(user['password'], password):
			error = 'Incorrect Password'

		if error is None:
			session.clear()
			session['user_id'] = user['id']
			return redirect(url_for('index'))

		flash(error)

	return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
	user_id = session.get('user_id')

	if user_id is None:
		g.user = None
	else:
		g.user = get_db().execute(
			'SELECT * FROM user WHERE id =?', (user_id,)
		).fetchone()

@bp.route('/logout')
def logout():
	session.clear()
	return redirect(url_for('index'))

def login_required(view):
	@functools.wraps(view)
	def wrapped_view(**kwargs):
		if g.user is None:
			return redirect(url_for('auth.login'))

		return view(**kwargs)

	return wrapped_view