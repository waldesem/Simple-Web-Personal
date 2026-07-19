"""User info and decorators."""

from collections.abc import Callable
from functools import lru_cache, wraps
from typing import TYPE_CHECKING, get_type_hints

from flask import abort, current_app, g, request
from pydantic import ValidationError

from app.classes.enums import Roles
from app.utilities.utils import decode_token

if TYPE_CHECKING:
    from sqlite3 import Cursor


@lru_cache
def get_user(user_id: str) -> dict | None:
    """Retrieve user."""
    cur: Cursor = g.db.cursor()
    user = cur.execute(
        "SELECT id, fullname, username, email, role, blocked, deleted \
            FROM users WHERE id = ?",
        (user_id,),
    ).fetchone()
    return dict(user) if user else None


def authorize(role: Roles | None = None) -> Callable:
    """Decorate a function that checks a user."""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: tuple, **kwargs: dict) -> Callable:
            if not (header := request.headers.get("Authorization")):
                return abort(401)

            if not (decoded := decode_token(header[7:])):
                return abort(401)

            if user := get_user(decoded["id"]):
                if user["blocked"] or user["deleted"]:
                    return abort(403)

                if role and user["role"] not in role.value:
                    return abort(403)

                g.current_user = user

                return func(*args, **kwargs)

            return abort(400)

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
                return abort(500)

        return wrapper

    return decorator
