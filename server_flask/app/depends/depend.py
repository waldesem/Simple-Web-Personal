"""Get user."""

import getpass
from collections.abc import Callable
from functools import lru_cache, wraps
from typing import TYPE_CHECKING, get_type_hints

from flask import abort, current_app, g, request
from pydantic import ValidationError

from app.classes.enums import Roles

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


def authorize(role: Roles | None = None, *, refresh: bool = False) -> Callable:  # noqa: ARG001
    """Decorate a function that checks a user."""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: tuple, **kwargs: dict) -> Callable:
            username = getpass.getuser()
            user = get_user(username)
            # token = (
            #     request.get_json()["refresh_token"]
            #     if refresh
            #     else request.headers["Authorization"]
            # )
            # if (decoded := decode_token(token, refresh=refresh)) and (
            #     user := get_current_user(decoded["id"])
            # ):
            #     g.user = user
            # else:
            #     abort(401)

            if not user or user["blocked"] or user["deleted"]:
                return abort(401)

            if role and user["role"] != role:
                return abort(403)

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
                    kwargs["json_data"] = model.parse_obj(data)
                if model := type_hints.get("json_query"):
                    kwargs["json_query"] = model(**request.args)
                if model := type_hints.get("table"):
                    kwargs["table"] = model.parse_obj(kwargs["table"])

                return func(*args, **kwargs)

            except ValidationError as exc:
                current_app.logger.warning(exc)
                return abort(400)

        return wrapper

    return decorator
