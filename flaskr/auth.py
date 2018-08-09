import functools

from flask import (
	Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash

from flaskr.model.user import *
from flaskr.model.coach import *

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
	all_coaches = get_all_coaches()

	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		coach_id = request.form['coach']

		error = None

		coach = get_coach(coach_id)

		if not username:
			error = 'You need a username'
		elif not password:
			error = 'You need a password'
		elif not coach_id or not coach:
			error = 'You need a coach'
		elif user_exists(username):
			error = 'username {} is taken'.format(username)

		if error is None:
			create_user(username, password, coach_id)
			return redirect(url_for('auth.login'))

		flash (error)

	return render_template('auth/register.html', coaches = all_coaches)

@bp.route('/login', methods=('GET', 'POST'))
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		error = None
		user = fetch_user_by_name(username)

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
		g.user = fetch_user_by_id(user_id)

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