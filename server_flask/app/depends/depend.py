"""Get user."""

import getpass
from collections.abc import Callable
from functools import lru_cache, wraps
from typing import TYPE_CHECKING

from flask import Response, abort, g

if TYPE_CHECKING:
    import sqlite3


@lru_cache
def get_user(username: str) -> dict | None:
    """Retrieve user."""
    cur: sqlite3.Cursor = g.db.cursor()
    user = cur.execute(
        "SELECT id, fullname, username, email, role, created,\
        pswd_create, change_pswd, blocked, deleted, attempt\
        FROM users WHERE username = ?",
        (username,),
    ).fetchone()
    return dict(user) if user else None


def auth_required() -> Callable:
    """Decorate a function that checks a user."""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: tuple, **kwargs: dict) -> Response | Callable:
            username = getpass.getuser().lower()
            user = get_user(username)
            if not user or user.blocked or user.deleted:
                return abort(401)
            g.current_user = user
            return func(*args, **kwargs)

        return wrapper

    return decorator
