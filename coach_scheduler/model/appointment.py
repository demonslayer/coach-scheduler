from coach_scheduler.db import get_db

def fetch_appointments_for_coach(coach_id):
	return get_db().execute(
		'SELECT * FROM appointment WHERE coach_id = ? ORDER BY start_time DESC', 
		(coach_id,)
	).fetchall()

def fetch_appointments_for_user(user_id):
	return get_db().execute(
		'SELECT * FROM appointment WHERE user_id = ? ORDER BY start_time DESC', 
		(user_id,)
	).fetchall()

def appointment_exists(coach_id, date):
	return get_db().execute(
		'SELECT * FROM appointment WHERE coach_id = ? AND start_time = ?',
		(coach_id, date)
	).fetchone() is not None

def create_appointment(date, coach_id, user_id):
	db = get_db()
	db.execute(
		'INSERT INTO appointment (start_time, coach_id, user_id) VALUES (?, ?, ?)',
		(date, coach_id, user_id)
	)
	db.commit()