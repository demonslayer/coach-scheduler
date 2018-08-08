from flask import (
	Blueprint, flash, g, redirect, render_template, request, url_for
)

from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

from datetime import datetime

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
	db = get_db()
	all_appointments = db.execute(
		'SELECT * FROM appointment WHERE coach_id = ? ORDER BY start_time DESC', 
		(g.user['coach_id'],)
	).fetchall()

	if request.method == 'POST':
		date = request.form['date']
		time = request.form['time']
		coach_id = g.user['coach_id']
		error = None

		if not time or not date:
			error = 'Please choose an appointment time'
		else:
			converted_date = datetime.strptime(date + " " + time, '%Y-%m-%d %H')

			existing_appointments = db.execute(
				'SELECT * FROM appointment WHERE coach_id = ? AND start_time = ?',
				(coach_id, converted_date)
			).fetchone()

			if existing_appointments is not None:
				error  = "Your coach already has an appointment at that time"

		if error is not None:
			flash(error)
		else:
			print(date + " " + time)
			print(converted_date)
			db.execute(
				'INSERT INTO appointment (start_time, coach_id, user_id) VALUES (?, ?, ?)',
				(converted_date, coach_id, g.user['id'])
			)
			db.commit()
			return redirect(url_for('schedule.index'))

	return render_template('schedule/create.html', appointments = all_appointments)