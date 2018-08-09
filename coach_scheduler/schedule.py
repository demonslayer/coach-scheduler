from flask import (
	Blueprint, flash, g, redirect, render_template, request, url_for
)

from werkzeug.exceptions import abort

from coach_scheduler.auth import login_required
from coach_scheduler.db import get_db
from coach_scheduler.model.coach import *
from coach_scheduler.model.appointment import *

from datetime import datetime

bp = Blueprint('schedule', __name__)

@bp.route('/')
@login_required
def index():
	appointments = fetch_appointments_for_user(g.user['id'])

	coach = get_coach(g.user['coach_id'])

	return render_template('schedule/index.html', coach=coach['name'], appointments = appointments)

@bp.route('/schedule', methods=('GET', 'POST'))
@login_required
def schedule():
	appointments = fetch_appointments_for_coach(g.user['coach_id'])
	coach = get_coach(g.user['coach_id'])

	if request.method == 'POST':
		date = request.form['date']
		time = request.form['time']
		coach_id = g.user['coach_id']
		error = None

		if not time or not date:
			error = 'Please choose an appointment time'
		else:
			converted_date = datetime.strptime(date + " " + time, '%Y-%m-%d %H')

			if appointment_exists(coach_id, converted_date):
				error  = coach['name'] + " already has an appointment at that time"

		if error is not None:
			flash(error)
		else:
			create_appointment(converted_date, coach_id, g.user['id'])
			return redirect(url_for('schedule.index'))

	return render_template('schedule/schedule.html', appointments = appointments, coach = coach['name'])