"""Routes."""

from typing import Literal

from flask import Blueprint, Response, g, jsonify

from app.depends.depend import authorize

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.get("/session")
@authorize()
def get_session() -> tuple[Response, Literal[200]]:
    """Retrieve a session."""
    return jsonify(g.current_user), 200
