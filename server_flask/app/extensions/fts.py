"""Full-text search module."""

import sqlite3

from flask import Flask


class FullTextSearch:
    """Full-text search extension."""

    def __init__(self) -> None:
        """Init."""

    def init_app(self, app: Flask) -> None:
        """Initialize the app with extension defaults."""
        if not hasattr(app, "extensions"):
            app.extensions = {}
        app.extensions["fts"] = self

        with app.app_context(), sqlite3.connect(app.config["DATABASE_URI"]) as conn:
            conn.execute(
                """
                CREATE VIRTUAL TABLE IF NOT EXISTS persons_fts
                USING fts3(surname, firstname, patronymic, birthday,
                birthplace, citizenship, dual, snils, inn, marital, addition,
                created content='persons', content_rowid='id', tokenize = 'unicode61')
                """,
            )

            cur = conn.cursor()

            cur.execute(
                """
                INSERT OR IGNORE INTO persons_fts(rowid, surname, firstname,
                patronymic, birthday, birthplace, citizenship, dual, snils,
                inn, marital, addition, created) SELECT id, surname, firstname,
                patronymic, birthday, birthplace, citizenship, dual, snils, inn,
                marital, addition, created FROM persons;
                """,
            )

            cur.execute(
                """
                CREATE TRIGGER IF NOT EXISTS persons_ai AFTER INSERT ON persons
                BEGIN INSERT INTO persons_fts(rowid, surname, firstname, patronymic,
                birthday, birthplace, citizenship, dual, snils, inn, marital,
                addition, created) VALUES (new.id, new.surname, new.firstname,
                new.patronymic, new.birthday, new.birthplace, new.citizenship,
                new.dual, new.snils, new.inn, new.marital, new.addition,
                created); END;
                """,
            )

            cur.execute(
                """
                CREATE TRIGGER IF NOT EXISTS persons_ad AFTER DELETE ON persons
                BEGIN INSERT INTO persons_fts(persons_fts, rowid, surname, firstname,
                patronymic, birthday, birthplace, citizenship, dual, snils, inn,
                marital, addition, created) VALUES('delete', old.id, old.surname,
                old.firstname, old.patronymic, old.birthday, old.birthplace,
                old.citizenship, old.dual, old.snils, old.inn, old.marital,
                old.addition, old.created); END;
                """,
            )

            cur.execute(
                """
                CREATE TRIGGER IF NOT EXISTS persons_au AFTER UPDATE ON persons
                BEGIN INSERT INTO persons_fts(persons_fts, rowid, surname, firstname,
                patronymic, birthday, birthplace, citizenship, dual, snils, inn,
                marital, addition, created) VALUES('delete', old.id, old.surname,
                old.firstname, old.patronymic, old.birthday, old.birthplace,
                old.citizenship, old.dual, old.snils, old.inn, old.marital,
                old.addition, old.created);
                INSERT INTO persons_fts(rowid, surname, firstname, patronymic,
                birthday, birthplace, citizenship, dual, snils, inn, marital,
                addition, created) VALUES(new.id, new.surname, new.firstname,
                new.patronymic, new.birthday, new.birthplace, new.citizenship,
                new.dual, new.snils, new.inn, new.marital, new.addition,
                new.created); END;
                """,
            )

            conn.commit()
