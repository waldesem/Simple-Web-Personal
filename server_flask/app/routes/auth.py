"""Routes."""

from flask import Blueprint, Response, g, jsonify

from app.depends.depend import authorize

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.get("/session")
@authorize()
def get_session() -> Response:
    """Retrieve a session."""
    return jsonify(g.current_user), 200
