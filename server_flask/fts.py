"""Full-text search module."""

import sqlite3

import click

from config import Config


@click.command()
def create_fullsearch() -> None:
    """Create full-text search."""
    try:
        conn = sqlite3.connect(Config.DATABASE_URI)
        conn.execute(
            """
            CREATE VIRTUAL TABLE IF NOT EXISTS persons_fts
            USING fts3(surname, firstname, patronymic, birthday,
            birthplace, citizenship, dual, snils, inn, marital, addition,
            created content='persons', content_rowid='id',
            tokenize = 'unicode61')
            """,
        )

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
