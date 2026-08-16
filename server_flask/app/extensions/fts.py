"""Full-text search module."""

import sqlite3

from flask import Flask


class FullTextSearch:
    """Full-text search extension."""

    def __init__(self) -> None:
        """Init."""
        self.app = None

    def init_app(self, app: Flask) -> None:
        """Initialize the app with extension defaults."""
        if not hasattr(app, "extensions"):
            app.extensions = {}
        app.extensions["fts"] = self
        self.app = app

        with app.app_context():
            try:
                conn = sqlite3.connect(app.config["DATABASE_URI"])
                conn.execute(
                    """
                    CREATE VIRTUAL TABLE IF NOT EXISTS persons_fts
                    USING fts3(surname, firstname, patronymic, birthday,
                    birthplace, citizenship, dual, snils, inn, marital, addition,
                    created content='persons', content_rowid='id',
                    tokenize = 'unicode61')
                    """,
                )

                # Лучше запускать этот разово вручную, либо проверять count.
                # INSERT OR IGNORE предотвратит ошибки дубликатов, если rowid совпадает.
                conn.execute(
                    """
                    INSERT OR IGNORE INTO persons_fts(rowid, surname, firstname,
                    patronymic, birthday, birthplace, citizenship, dual, snils,
                    inn, marital, addition, created) SELECT id, surname, firstname,
                    patronymic, birthday, birthplace, citizenship, dual, snils, inn,
                    marital, addition, created FROM persons;
                    """,
                )

                conn.execute(
                    """
                    CREATE TRIGGER IF NOT EXISTS persons_insert AFTER INSERT ON persons
                    BEGIN
                        INSERT INTO persons_fts(rowid, surname, firstname, patronymic,
                        birthday, birthplace, citizenship, dual, snils, inn, marital,
                        addition, created) VALUES (new.id, new.surname, new.firstname,
                        new.patronymic, new.birthday, new.birthplace, new.citizenship,
                        new.dual, new.snils, new.inn, new.marital, new.addition,
                        new.created);
                    END;
                    """,
                )

                conn.execute(
                    """
                    CREATE TRIGGER IF NOT EXISTS persons_delete AFTER DELETE ON persons
                    BEGIN DELETE FROM persons_fts WHERE rowid = old.id; END;
                    """,
                )

                conn.execute(
                    """
                    CREATE TRIGGER IF NOT EXISTS persons_update AFTER UPDATE ON persons
                    BEGIN
                        DELETE FROM persons_fts WHERE rowid = old.id;
                        INSERT INTO persons_fts(rowid, surname, firstname, patronymic,
                        birthday, birthplace, citizenship, dual, snils, inn, marital,
                        addition, created) VALUES (new.id, new.surname, new.firstname,
                        new.patronymic, new.birthday, new.birthplace, new.citizenship,
                        new.dual, new.snils, new.inn, new.marital, new.addition,
                        new.created);
                    END;
                    """,
                )
                conn.commit()
            finally:
                conn.close()
