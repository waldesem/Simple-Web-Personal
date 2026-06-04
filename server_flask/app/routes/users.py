"""Routes."""

from datetime import UTC, datetime
from typing import TYPE_CHECKING

from flask import Blueprint, Response, g, jsonify
from werkzeug.security import generate_password_hash

from app.depends.depend import validize
from app.models.model import Action, User

if TYPE_CHECKING:
    import sqlite3

bp = Blueprint("users", __name__, url_prefix="/users")


@bp.get("/")
def get_users() -> Response:
    """Retrieve a list of users or once user by id."""
    cur: sqlite3.Cursor = g.db.cursor()
    users = cur.execute(
        "SELECT id, fullname, username, email, role, created,\
        pswd_create, change_pswd, blocked, deleted, attempt FROM users",
    ).fetchall()
    return jsonify([dict(user) for user in users]), 200


@bp.post("/")
@validize()
def post_user(json_data: User) -> Response:
    """Create a new user."""
    cur: sqlite3.Cursor = g.db.cursor()
    if cur.execute(
        "SELECT * FROM users WHERE username = ? OR email = ?",
        (json_data.username, json_data.email),
    ).fetchone():
        return "", 200

    cur.execute(
        """INSERT INTO users
        (fullname, username, email, role, created, passhash,
        pswd_create, change_pswd, blocked, deleted, attempt)
        VALUES (?,?,?,?,?,?,?,?,?,?,?)
        """,
        (
            json_data.fullname,
            json_data.username,
            json_data.email,
            json_data.role,
            datetime.now(UTC),
            generate_password_hash("88888888"),
            datetime.now(UTC),
            True,
            False,
            False,
            0,
        ),
    )
    g.db.commit()
    return "", 201


@bp.post("/<int:user_id>")
def update_user(user_id: int, json_data: User) -> Response:
    """Change a user's role."""
    cur: sqlite3.Cursor = g.db.cursor()
    stmt = "UPDATE users SET role = ?, change_pswd = 1 WHERE id = ?"
    cur.execute(stmt, (json_data.role, user_id))
    g.db.commit()
    return "", 201


@bp.patch("/<int:user_id>")
def edit_user(user_id: int, json_data: Action) -> Response:
    """Change a user's information."""
    cur: sqlite3.Cursor = g.db.cursor()
    stmt = "UPDATE users SET "
    params = []
    if json_data.action == "reset":
        # Сбросить пароль пользователя и обнулить попытки входа
        stmt += "passhash = ?, attempt = 0, blocked = 0, change_pswd = 1"
        params.append(generate_password_hash("88888888"))
    elif json_data.action == "block":
        # Заблокировать или разблокировать пользователя
        stmt += "blocked = NOT blocked"
    elif json_data.action == "delete":
        # Удалить или восстановить пользователя
        stmt += "SET deleted = NOT deleted"
    cur.execute(stmt + " WHERE id = ?", (*params, user_id))
    g.db.commit()
    return "", 200
