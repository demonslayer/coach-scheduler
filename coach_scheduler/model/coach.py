from coach_scheduler.db import get_db

def get_all_coaches():
	return get_db().execute('SELECT * FROM coach').fetchall()

def get_coach(coach_id):
	return get_db().execute( 'SELECT * FROM coach WHERE id = ?', (coach_id,)).fetchone()

def appointment_exists(coach_id, date):
	return db.execute(
		'SELECT * FROM appointment WHERE coach_id = ? AND start_time = ?',
		(coach_id, date)
	).fetchone() is not None