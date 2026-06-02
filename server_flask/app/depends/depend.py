"""Get user."""

import getpass
from collections.abc import Callable
from functools import lru_cache, wraps
from typing import TYPE_CHECKING

from flask import Response, abort, g
from werkzeug.local import LocalProxy

if TYPE_CHECKING:
    import sqlite3

current_user = LocalProxy(lambda: get_user)


@lru_cache
def get_user() -> dict | None:
    """Retrieve the current user."""
    username = getpass.getuser()
    cur: sqlite3.Cursor = g.db.cursor()
    user = cur.execute(
        "SELECT * FROM users WHERE username = ?",
        (username.lower(),),
    ).fetchone()
    if user:
        return dict(user)
    return None


def auth_required() -> Callable:
    """Decorate a function that checks a user."""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: tuple, **kwargs: dict) -> Response | Callable:
            if not current_user or current_user.blocked or current_user.deleted:
                return abort(401)
            g.current_user = current_user
            return func(*args, **kwargs)

        return wrapper

    return decorator
