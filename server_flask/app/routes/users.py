"""Routes."""

from datetime import UTC, datetime
from typing import TYPE_CHECKING

from flask import Blueprint, Response, g, jsonify
from werkzeug.security import generate_password_hash

from app.classes.enums import Roles
from app.depends.depend import authorize, validize
from app.models.model import Action, User

if TYPE_CHECKING:
    import sqlite3

bp = Blueprint("users", __name__, url_prefix="/users")


@bp.get("/")
@authorize(Roles.admin)
def get_users() -> Response:
    """Retrieve a list of users or once user by id."""
    cur: sqlite3.Cursor = g.db.cursor()
    users = cur.execute(
        "SELECT id, fullname, username, email, role, created,\
        pswd_create, change_pswd, blocked, deleted, attempt FROM users",
    ).fetchall()
    return jsonify([dict(user) for user in users])


@bp.get("/<int:user_id>")
@validize()
@authorize(Roles.admin)
def edit_user(user_id: int, json_query: Action) -> Response:
    """Change a user's information."""
    cur: sqlite3.Cursor = g.db.cursor()
    stmt = "UPDATE users SET "
    params = []
    if json_query.action == "reset":
        stmt += "passhash = ?, attempt = 0, blocked = 0, change_pswd = 1"
        params.append(generate_password_hash("88888888"))
    elif json_query.action == "block":
        stmt += "blocked = NOT blocked"
    elif json_query.action == "delete":
        stmt += "deleted = NOT deleted"
    cur.execute(stmt + " WHERE id = ?", (*params, user_id))
    g.db.commit()
    return jsonify({"message": "success"})


@bp.post("/")
@validize()
@authorize(Roles.admin)
def post_user(json_data: User) -> Response:
    """Create a new user."""
    cur: sqlite3.Cursor = g.db.cursor()
    stmt = "SELECT * FROM users WHERE username = ? OR email = ?"
    if cur.execute(stmt, (json_data.username, json_data.email)).fetchone():
        return jsonify({"message": "success"})

    cur.execute(
        "INSERT INTO users\
        (fullname, username, email, role, created, passhash,\
        pswd_create, change_pswd, blocked, deleted, attempt)\
        VALUES (?,?,?,?,?,?,?,1,0,0,0)",
        (
            *json_data.dict().values(),
            datetime.now(UTC),
            generate_password_hash("88888888"),
            datetime.now(UTC),
        ),
    )
    g.db.commit()
    return jsonify({"message": "success"})


@bp.patch("/<int:user_id>")
@validize()
@authorize(Roles.admin)
def update_user(user_id: int, json_data: User) -> Response:
    """Change a user's role."""
    cur: sqlite3.Cursor = g.db.cursor()
    stmt = "UPDATE users SET role = ?, change_pswd = 1 WHERE id = ?"
    cur.execute(stmt, (json_data.role, user_id))
    g.db.commit()
    return jsonify({"message": "success"})
