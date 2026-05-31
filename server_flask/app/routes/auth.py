"""Routes."""

from dataclasses import asdict
from typing import TYPE_CHECKING, Literal

from flask import Blueprint, Response, abort, g, jsonify

from app.depends.depend import get_user

if TYPE_CHECKING:
    import sqlite3

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.get("/session")
def get_session() -> tuple[Response, Literal[200]]:
    """Retrieve a session."""
    cur: sqlite3.Cursor = g.db.cursor()
    session = get_user(cur)
    if not session:
        return abort(401)
    return jsonify(asdict(session)), 200
