"""Get user."""

import getpass
import sqlite3
from functools import lru_cache

from flask import abort

from app.data.classes import User


@lru_cache
def get_user(cur: sqlite3.Cursor) -> User:
    """Retrieve the current user."""
    username = getpass.getuser()
    user = cur.execute(
        "SELECT * FROM users WHERE username = ?",
        (username.lower(),),
    ).fetchone()
    if user:
        return User(*user)
    return abort(404)
