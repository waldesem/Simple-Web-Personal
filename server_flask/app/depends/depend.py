"""Get user."""

import getpass  # noqa: F401
from collections.abc import Callable
from functools import lru_cache, wraps
from typing import TYPE_CHECKING, get_type_hints

from flask import abort, current_app, g, request
from pydantic import ValidationError

from app.classes.enums import Roles
from app.utilities.utils import decode_token  # noqa: F401, RUF100

if TYPE_CHECKING:
    import sqlite3


@lru_cache
def get_user(user_id: str) -> dict | None:
    """Retrieve user."""
    cur: sqlite3.Cursor = g.db.cursor()
    user = cur.execute(
        "SELECT id, fullname, username, email, role FROM users WHERE id = ?",
        (user_id,),
    ).fetchone()
    return dict(user) if user else None


def authorize(role: Roles | None = None) -> Callable:
    """Decorate a function that checks a user."""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: tuple, **kwargs: dict) -> Callable:
            # username = getpass.getuser()
            if (
                (header := request.headers.get("Authorization"))
                and (decoded := decode_token(header[7:]))
                and (user := get_user(decoded["id"]))
            ):
                g.user = user
            else:
                abort(401)

            if not user or user["blocked"] or user["deleted"]:
                return abort(401)

            if role and user["role"] != role.value:
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
