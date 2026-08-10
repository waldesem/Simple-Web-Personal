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
            conn.enable_load_extension(True)  # noqa: FBT003

            conn.execute("select load_extension('./fts3.so')")

            conn.execute(
                """
                CREATE VIRTUAL TABLE persons_fts
                USING fts3(surname, firstname, patronymic, birthday,
                birthplace, citizenship, dual, snils, inn, marital, addition,
                content='persons', content_rowid='id')
                """,
            )

            cur = conn.cursor()

            cur.execute(
                """
                INSERT INTO persons_fts(rowid, surname, firstname, patronymic,
                birthday, birthplace, citizenship, dual, snils, inn, marital, addition)
                SELECT id, surname, firstname, patronymic, birthday, birthplace,
                citizenship, dual, snils, inn, marital, addition FROM persons;
                """,
            )

            cur.execute(
                """
                CREATE TRIGGER IF NOT EXISTS persons_ai AFTER INSERT ON persons BEGIN
                INSERT INTO persons_fts(rowid, surname, firstname, patronymic, birthday,
                birthplace, citizenship, dual, snils, inn, marital, addition)
                VALUES (new.id, new.surname, new.firstname, new.patronymic,
                new.birthday, new.birthplace, new.citizenship, new.dual,
                new.snils, new.inn, new.marital, new.addition); END;
                """,
            )

            cur.execute(
                """
                CREATE TRIGGER IF NOT EXISTS persons_ad AFTER DELETE ON persons BEGIN
                INSERT INTO persons_fts(persons_fts, rowid, surname, firstname,
                patronymic, birthday, birthplace, citizenship, dual, snils, inn,
                marital, addition) VALUES('delete', old.id, old.surname, old.firstname,
                old.patronymic, old.birthday, old.birthplace, old.citizenship, old.dual,
                old.snils, old.inn, old.marital, old.addition); END;
                """,
            )

            cur.execute(
                """
                CREATE TRIGGER IF NOT EXISTS persons_au AFTER UPDATE ON persons BEGIN
                INSERT INTO persons_fts(persons_fts, rowid, surname, firstname,
                patronymic, birthday, birthplace, citizenship, dual, snils, inn,
                marital, addition) VALUES('delete', old.id, old.surname, old.firstname,
                old.patronymic, old.birthday, old.birthplace, old.citizenship, old.dual,
                old.snils, old.inn, old.marital, old.addition);
                INSERT INTO persons_fts(rowid, surname, firstname, patronymic, birthday,
                birthplace, citizenship, dual, snils, inn, marital, addition)
                VALUES(new.id, new.surname, new.firstname, new.patronymic,
                new.birthday, new.birthplace, new.citizenship, new.dual,
                new.snils, new.inn, new.marital, new.addition);END;
                """,
            )
