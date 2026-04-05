"""Utils module."""

import getpass
import sqlite3
from enum import Enum
from functools import lru_cache
from pathlib import Path

from flask import current_app


class Item(Enum):
    """Item categories."""

    ADDRESSES = "addresses"
    AFFILATIONS = "affilations"
    CHECKS = "checks"
    CONTACTS = "contacts"
    DOCUMENTS = "documents"
    EDUCATIONS = "educations"
    INQUIRIES = "inquiries"
    INVESTIGATIONS = "investigations"
    PREVIOUS = "previous"
    POLIGRAFS = "poligrafs"
    STAFFS = "staffs"
    WORKPLACES = "workplaces"


@lru_cache
def get_user_id(cur: sqlite3.Cursor) -> int | None:
    """Retrieve the current user."""
    username = getpass.getuser()
    user = cur.execute(
        "SELECT id FROM users WHERE username = ?",
        (username.lower(),),
    ).fetchone()
    return user["id"] if user else None


def create_dest(person: dict) -> str:
    """Create destination."""
    destination = Path(
        current_app.config["BASE_PATH"],
        "Главный офис",
        person["surname"][0],
        "{}-{} {} {}".format(
            person["id"],
            person["surname"],
            person["firstname"],
            person.get("patronymic", ""),
        ).rstrip(),
    )
    destination.mkdir(parents=True, exist_ok=True)
    return str(destination)


def make_dicts(cursor: sqlite3.Cursor, row: sqlite3.Row) -> dict:
    """Convert SQL row to dictionary."""
    return {cursor.description[idx][0]: value for idx, value in enumerate(row)}
