BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS addresses (
	id INTEGER NOT NULL, 
	"view" VARCHAR(255) NOT NULL, 
	address TEXT NOT NULL, 
	created DATETIME NOT NULL, 
	person_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (id), 
	FOREIGN KEY(person_id) REFERENCES persons (id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS affilations (
	id INTEGER NOT NULL, 
	"view" VARCHAR(255) NOT NULL, 
	organization TEXT NOT NULL, 
	inn VARCHAR(255) NOT NULL, 
	created DATETIME NOT NULL, 
	person_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (id), 
	FOREIGN KEY(person_id) REFERENCES persons (id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS checks (
	id INTEGER NOT NULL, 
	workplace TEXT NOT NULL, 
	document TEXT NOT NULL, 
	inn TEXT NOT NULL, 
	debt TEXT NOT NULL, 
	bankruptcy TEXT NOT NULL, 
	bki TEXT NOT NULL, 
	courts TEXT NOT NULL, 
	affilation TEXT NOT NULL, 
	terrorist TEXT NOT NULL, 
	mvd TEXT NOT NULL, 
	internet TEXT NOT NULL, 
	cronos TEXT NOT NULL, 
	cros TEXT NOT NULL, 
	addition TEXT NOT NULL, 
	comment TEXT NOT NULL, 
	conclusion TEXT NOT NULL, 
	created DATETIME NOT NULL, 
	person_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (id), 
	FOREIGN KEY(person_id) REFERENCES persons (id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS contacts (
	id INTEGER NOT NULL, 
	"view" VARCHAR(255) NOT NULL, 
	contact VARCHAR(255) NOT NULL, 
	created DATETIME NOT NULL, 
	person_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (id), 
	FOREIGN KEY(person_id) REFERENCES persons (id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS documents (
	id INTEGER NOT NULL, 
	"view" VARCHAR(255) NOT NULL, 
	series VARCHAR(255) NOT NULL, 
	digits VARCHAR(255) NOT NULL, 
	agency TEXT NOT NULL, 
	issue DATE NOT NULL, 
	created DATETIME NOT NULL, 
	person_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (id), 
	FOREIGN KEY(person_id) REFERENCES persons (id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS educations (
	id INTEGER NOT NULL, 
	"view" VARCHAR(255) NOT NULL, 
	institution TEXT NOT NULL, 
	finished INTEGER NOT NULL, 
	specialty TEXT NOT NULL, 
	created DATETIME NOT NULL, 
	person_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (id), 
	FOREIGN KEY(person_id) REFERENCES persons (id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS inquiries (
	id INTEGER NOT NULL, 
	info TEXT NOT NULL, 
	initiator VARCHAR(255) NOT NULL, 
	origins VARCHAR(255) NOT NULL, 
	created DATETIME NOT NULL, 
	person_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (id), 
	FOREIGN KEY(person_id) REFERENCES persons (id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS investigations (
	id INTEGER NOT NULL, 
	theme VARCHAR(255) NOT NULL, 
	info TEXT NOT NULL, 
	created DATETIME NOT NULL, 
	person_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (id), 
	FOREIGN KEY(person_id) REFERENCES persons (id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS persons (
	id INTEGER NOT NULL, 
	surname VARCHAR(255) NOT NULL, 
	firstname VARCHAR(255) NOT NULL, 
	patronymic VARCHAR(255) NOT NULL, 
	birthday DATE NOT NULL, 
	birthplace TEXT NOT NULL, 
	citizenship VARCHAR(255) NOT NULL, 
	dual VARCHAR(255) NOT NULL, 
	snils VARCHAR(255) NOT NULL, 
	inn VARCHAR(255) NOT NULL, 
	marital VARCHAR(255) NOT NULL, 
	addition TEXT NOT NULL, 
	destination TEXT NOT NULL, 
	created DATETIME NOT NULL, 
	editable BOOLEAN NOT NULL, 
	user_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (id), 
	FOREIGN KEY(user_id) REFERENCES users (id)
);
CREATE TABLE IF NOT EXISTS poligrafs (
	id INTEGER NOT NULL, 
	theme VARCHAR(255) NOT NULL, 
	results TEXT NOT NULL, 
	conclusion VARCHAR(255) NOT NULL, 
	created DATETIME NOT NULL, 
	person_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (id), 
	FOREIGN KEY(person_id) REFERENCES persons (id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS previous (
	id INTEGER NOT NULL, 
	surname VARCHAR(255) NOT NULL, 
	firstname VARCHAR(255) NOT NULL, 
	patronymic VARCHAR(255) NOT NULL, 
	changed VARCHAR(255) NOT NULL, 
	reason TEXT NOT NULL, 
	created DATETIME NOT NULL, 
	person_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (id), 
	FOREIGN KEY(person_id) REFERENCES persons (id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS staffs (
	id INTEGER NOT NULL, 
	position TEXT NOT NULL, 
	department TEXT NOT NULL, 
	created DATETIME NOT NULL, 
	person_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (id), 
	FOREIGN KEY(person_id) REFERENCES persons (id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS users (
	id INTEGER NOT NULL, 
	fullname VARCHAR(255) NOT NULL, 
	username VARCHAR(255) NOT NULL, 
	email VARCHAR(255) NOT NULL, 
	created DATETIME NOT NULL, 
	passhash VARCHAR(255) NOT NULL, 
	pswd_create DATETIME NOT NULL, 
	change_pswd BOOLEAN NOT NULL, 
	blocked BOOLEAN NOT NULL, 
	deleted BOOLEAN NOT NULL, 
	attempt INTEGER NOT NULL, 
	role VARCHAR NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (id), 
	UNIQUE (username), 
	UNIQUE (email)
);
CREATE TABLE IF NOT EXISTS workplaces (
	id INTEGER NOT NULL, 
	now_work BOOLEAN NOT NULL, 
	starts DATE, 
	finished DATE, 
	workplace VARCHAR(255) NOT NULL, 
	address TEXT NOT NULL, 
	position TEXT NOT NULL, 
	reason TEXT NOT NULL, 
	created DATETIME NOT NULL, 
	person_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (id), 
	FOREIGN KEY(person_id) REFERENCES persons (id) ON DELETE CASCADE
);
CREATE INDEX ix_persons_firstname ON persons (firstname);
CREATE INDEX ix_persons_surname ON persons (surname);
CREATE INDEX ix_persons_patronymic ON persons (patronymic);
CREATE INDEX ix_previous_person_id ON previous (person_id);
CREATE INDEX ix_educations_person_id ON educations (person_id);
CREATE INDEX ix_staffs_person_id ON staffs (person_id);
CREATE INDEX ix_documents_person_id ON documents (person_id);
CREATE INDEX ix_addresses_person_id ON addresses (person_id);
CREATE INDEX ix_contacts_person_id ON contacts (person_id);
CREATE INDEX ix_workplaces_person_id ON workplaces (person_id);
CREATE INDEX ix_affilations_person_id ON affilations (person_id);
CREATE INDEX ix_checks_person_id ON checks (person_id);
CREATE INDEX ix_poligrafs_person_id ON poligrafs (person_id);
CREATE INDEX ix_investigations_person_id ON investigations (person_id);
CREATE INDEX ix_inquiries_person_id ON inquiries (person_id);
COMMIT;