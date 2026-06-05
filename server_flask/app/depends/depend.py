"""Get user."""

import getpass
from collections.abc import Callable
from functools import lru_cache, wraps
from typing import TYPE_CHECKING, get_type_hints

from flask import abort, g, request
from pydantic import ValidationError

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
        (username.lower(),),
    ).fetchone()
    return dict(user) if user else None


def authorize() -> Callable:
    """Decorate a function that checks a user."""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: tuple, **kwargs: dict) -> Callable:
            username = getpass.getuser()
            user = get_user(username)
            if not user or user.blocked or user.deleted:
                return abort(401)
            g.current_user = user
            return func(*args, **kwargs)

        return wrapper

    return decorator


def validize() -> Callable:
    """Decorate a function for validate data using Pydantic models."""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: tuple, **kwargs: dict) -> Callable:
            try:
                type_hints = get_type_hints(func)
                if model := type_hints.get("json_data"):
                    data = request.get_json()
                    kwargs["json_data"] = model(**data)
                if model := type_hints.get("json_query"):
                    kwargs["json_query"] = model(**request.args)
                return func(*args, **kwargs)

            except ValidationError:
                return abort(400)

        return wrapper

    return decorator
