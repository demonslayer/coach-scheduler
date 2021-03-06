DROP TABLE IF EXISTS coach;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS appointment;

CREATE TABLE coach (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT NOT NULL
);

CREATE TABLE user (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	username TEXT NOT NULL,
	password TEXT NOT NULL,
	coach_id INTEGER NOT NULL,
	FOREIGN KEY (coach_id) REFERENCES coach (id)
);

CREATE TABLE appointment (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	start_time datetime NOT NULL,
	coach_id INTEGER NOT NULL,
	user_id INTEGER NOT NULL,
	FOREIGN KEY (coach_id) REFERENCES coach (id),
	FOREIGN KEY (user_id) REFERENCES user (id)
);

/* initializing with some "dummy" coaches the user can choose from */
INSERT INTO coach (name) VALUES ('Morgan');
INSERT INTO coach (name) VALUES ('Bob');
INSERT INTO coach (name) VALUES ('Sara');