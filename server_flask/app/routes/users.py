"""Routes."""

from datetime import datetime, timezone
from typing import TYPE_CHECKING

from flask import Blueprint, Response, g, jsonify, request
from werkzeug.security import generate_password_hash

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
def post_user() -> Response:
    """Create a new user."""
    cur: sqlite3.Cursor = g.db.cursor()
    resume: dict = request.get_json()
    if cur.execute(
        "SELECT * FROM users WHERE username = ? OR email = ?",
        (resume["username"], resume["email"]),
    ).fetchone():
        return "", 204

    cur.execute(
        """INSERT INTO users
        (fullname, username, email, role, created, passhash,
        pswd_create, change_pswd, blocked, deleted, attempt)
        VALUES (?,?,?,?,?,?,?,?,?,?,?)
        """,
        (
            resume["fullname"],
            resume["username"],
            resume["email"],
            resume["role"],
            datetime.now(timezone.utc).isoformat(),  # noqa: UP017
            generate_password_hash("88888888"),
            datetime.now(timezone.utc).isoformat(),  # noqa: UP017
            True,
            False,
            False,
            0,
        ),
    )
    g.db.commit()

    return "", 201


@bp.post("/<int:user_id>")
def update_user(user_id: int) -> Response:
    """Create a new user."""
    cur: sqlite3.Cursor = g.db.cursor()
    form: dict = request.get_json()
    stmt = "UPDATE users SET {} WHERE id = ?".format(  # noqa: S608
        ",".join(f"{k}=?" for k in form),
    )
    cur.execute(stmt, (*form.values(), user_id))
    g.db.commit()
    return "", 201


@bp.patch("/<int:user_id>")
def patch_user(user_id: int) -> Response:
    """Change a user's information in the database."""
    cur: sqlite3.Cursor = g.db.cursor()
    actions: dict = request.get_json()
    match actions["action"]:
        case "reset":
            # Сбросить пароль пользователя и обнулить попытки входа
            cur.execute(
                """
                UPDATE users SET
                passhash = ?, attempt = 0, blocked = 0, change_pswd = 1
                WHERE id = ?
                """,
                (generate_password_hash("88888888"), user_id),
            )
        case "block":
            # Заблокировать или разблокировать пользователя
            cur.execute(
                "UPDATE users SET blocked = NOT blocked WHERE id = ?",
                (user_id,),
            )
        case "delete":
            # Удалить или восстановить пользователя
            cur.execute(
                "UPDATE users SET deleted = NOT deleted WHERE id = ?",
                (user_id,),
            )
        case _:
            cur.execute(
                "UPDATE users SET role=? WHERE id=?",
                (actions["action"], user_id),
            )
    return "", 200
