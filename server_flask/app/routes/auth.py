"""Routes."""

from dataclasses import asdict

from flask import Blueprint, Response, g, jsonify

from app.depends.depend import auth_required

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.get("/session")
@auth_required
def get_session() -> Response:
    """Retrieve a session."""
    return jsonify(asdict(g.current_user)), 200
