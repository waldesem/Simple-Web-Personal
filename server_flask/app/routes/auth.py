"""Routes."""

from datetime import UTC, datetime
from typing import TYPE_CHECKING, Literal

from flask import Blueprint, Response, abort, g, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash

from app.depends.depend import authorize, validize
from app.models.model import Login, Update
from app.utilities.utils import create_token, decode_token

if TYPE_CHECKING:
    import sqlite3

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.post("/login")
@validize()
def post_login(json_data: Login) -> tuple[Response, Literal[201]]:
    """Handle the login process."""
    cur: sqlite3.Cursor = g.db.cursor()
    stmt = "SELECT * FROM users WHERE username = ?"
    result = cur.execute(stmt, (json_data.username,)).fetchone()
    user = dict(result) if result else None

    if not user or user["blocked"] or user["deleted"]:
        return jsonify({"message": "invalid"}), 201

    if not check_password_hash(user["passhash"], json_data.password):
        stmt = "UPDATE users SET "
        params = []
        if user["attempt"] < 5:
            stmt += "attempt = ?"
            params.append(user["attempt"] + 1)
        else:
            stmt += "blocked = 1"
        cur.execute(stmt + " WHERE id = ?", (*params, user["id"]))
        g.db.commit()
        return jsonify({"message": "invalid"}), 201

    delta_change = datetime.now() - user["pswd_create"]
    if not user["change_pswd"] and delta_change.days < 365:
        if user["attempt"]:
            stmt = "UPDATE users SET attempt = 0 WHERE id = ?"
            cur.execute(stmt, (user["id"],))
            g.db.commit()
        return jsonify(
            {
                "message": "success",
                "access_token": create_token(user["id"]),
                "refresh_token": create_token(user["id"], "REFRESH"),
            },
        ), 201
    return jsonify({"message": "denied"}), 201


@bp.patch("/login")
@validize()
def patch_login(json_data: Update) -> tuple[Response, Literal[200]]:
    """Handle the login process."""
    cur: sqlite3.Cursor = g.db.cursor()
    stmt = "SELECT * FROM users WHERE username = ?"
    result = cur.execute(stmt, (json_data.username,)).fetchone()
    user = dict(result) if result else None

    if not user or user["blocked"] or user["deleted"]:
        return jsonify({"message": "invalid"}), 200

    stmt = "UPDATE users SET "
    if not check_password_hash(user["passhash"], json_data.password):
        params = []
        if user["attempt"] < 5:
            stmt += "attempt = ?"
            params.append(user["attempt"] + 1)
        else:
            stmt += "blocked = 1"
        cur.execute(stmt + " WHERE id = ?", (*params, user["id"]))
        g.db.commit()
        return jsonify({"message": "invalid"}), 200

    stmt += "passhash = ?, pswd_create =?, attempt = 0, change_pswd = 0 WHERE id = ?"
    cur.execute(
        stmt,
        (
            generate_password_hash(json_data.new_pswd),
            datetime.now(UTC),
            user["id"],
        ),
    )
    g.db.commit()
    return jsonify({"message": "updated"}), 200


@bp.post("/refresh")
def refresh_token() -> tuple[Response, Literal[201]]:
    """Refresh the access token."""
    refresh_token = request.get_json()
    if decoded := decode_token(refresh_token, refresh=True):
        return jsonify(
            {
                "access_token": create_token(decoded["id"]),
            },
        ), 201
    return abort(400)


@bp.get("/session")
@authorize()
def get_session() -> tuple[Response, Literal[200]]:
    """Retrieve a session."""
    return jsonify(g.current_user), 200
