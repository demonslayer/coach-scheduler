from flask import (
	Blueprint, flash, g, redirect, render_template, request, url_for
)

from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('schedule', __name__)

@bp.route('/')
def index():

	if g.user is None:
		return render_template('auth/login.html')
	
	db = get_db();
	appointments = db.execute(
		'SELECT * FROM appointment WHERE user_id = ? ORDER BY start_time DESC', 
		(g.user['id'],)
	).fetchall()

	coach = db.execute(
		'SELECT * FROM coach WHERE id = ?', (g.user['coach_id'],)
	).fetchone()

	return render_template('schedule/index.html', coach=coach['name'], appointments = appointments)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
	if request.method == 'POST':
		start_time = request.form['start_time']
		coach_id = g.user['coach_id']
		error = None

		if not start_time:
			error = 'Please choose an appointment time'

		if error is not None:
			flash(error)
		else:
			db = get_db()
			db.execute(
				'INSERT INTO appointment (start_time, coach_id, user_id) VALUES (?, ?, ?)',
				(start_time, coach_id, g.user['id'])
			)
			db.commit()
			return redirect(url_for('schedule.index'))

	return render_template('schedule/create.html')