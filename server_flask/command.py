"""Command line module."""

import sqlite3
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path

import click
from werkzeug.security import generate_password_hash

from config import Config


class Actions(Enum):
    """Actions."""

    BLOCK = "block"
    RESET = "reset"
    DELETE = "delete"


class Roles(Enum):
    """Roles."""

    ADMIN = "admin"
    GUEST = "guest"
    USER = "user"


@click.group()
def cli() -> None:
    """Cli group."""


@cli.command()
@click.argument("filename", type=click.Path(exists=True))
def initdb(filename: Path) -> None:
    """Init database.

    Example:
        python3 command.py initdb tables.sql

    """
    with (
        Path.open(filename, "r", encoding="utf-8") as f,
        sqlite3.connect(Config.DATABASE_URI) as conn,
    ):
        file = f.read()
        cur = conn.cursor()
        cur.executescript(file)
        conn.commit()
        click.secho("Database successfully created.", bg="green")


@cli.command()
@click.option("--user_id", type=int, default=None)
def user(user_id: int) -> None:
    """Retrieve a list of users or once user by id.

    Example:
        python3 command.py user
        python3 command.py user --user_id=1

    """
    with sqlite3.connect(Config.DATABASE_URI) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        stmt = """
            SELECT id, fullname, username, email, role, created,
            pswd_create, change_pswd, blocked, deleted, attempt FROM users
            """
        args = ()
        if user_id:
            stmt += " WHERE id = ?"
            args = (user_id,)
        for user in cur.execute(stmt, args).fetchall():
            for col, row in dict(user).items():
                click.echo(f"| {col} | {row} |")
                click.echo("-" * (len(col) + len(str(row)) + 7))
            click.echo(" ")


@cli.command()
@click.argument("fullname")
@click.argument("username")
@click.argument("email")
@click.option("--role", type=click.Choice(Roles))
def create(
    fullname: str,
    username: str,
    email: str,
    role: Roles,
) -> None:
    """Create a new user.

    Example:
        python3 command.py create "Super User" superadmin 'super@host.ru' --role=admin

    """
    with sqlite3.connect(Config.DATABASE_URI) as conn:
        cur = conn.cursor()
        if cur.execute(
            "SELECT * FROM users WHERE username = ? OR email = ?",
            (username.lower().strip(), email.strip()),
        ).fetchone():
            click.secho(f"User {username} already exists or email is taken", bg="red")
        else:
            user_id = cur.execute(
                """INSERT INTO users
                (fullname, username, email, role, created, passhash,
                pswd_create, change_pswd, blocked, deleted, attempt)
                VALUES (?,?,?,?,?,?,?,?,?,?,?)
                """,
                (
                    fullname.upper().strip(),
                    username.lower().strip(),
                    email.strip(),
                    role,
                    datetime.now(timezone.utc).isoformat(),  # noqa: UP017
                    generate_password_hash(Config.DEFAULT_PASSWORD),
                    datetime.now(timezone.utc).isoformat(),  # noqa: UP017
                    True,
                    False,
                    False,
                    0,
                ),
            ).lastrowid
            conn.commit()
            click.secho(f"User with ID {user_id} created", bg="green")


@cli.command()
@click.argument("user_id", type=int)
@click.option("--action", type=click.Choice(Actions))
def edit(user_id: int, action: Actions) -> None:
    """Change a user's information in the database.

    Example:
        python3 command.py edit 1 --action=block

    """
    with sqlite3.connect(Config.DATABASE_URI) as conn:
        cur = conn.cursor()
        if not cur.execute("SELECT id FROM users WHERE id = ?", (user_id,)).fetchone():
            click.secho(f"User ID {user_id} not found", bg="red")
        else:
            match action:
                case "reset":
                    # Сбросить пароль пользователя и обнулить попытки входа
                    cur.execute(
                        """
                        UPDATE users SET
                        passhash = ?, attempt = 0, blocked = 0, change_pswd = 1
                        WHERE id = ?
                        """,
                        (generate_password_hash(Config.DEFAULT_PASSWORD), user_id),
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
            click.secho(f"User {action} succefully", bg="green")


@cli.command()
@click.argument("user_id", type=int)
@click.option("--role", type=click.Choice(Roles))
def role(user_id: int, role: Roles) -> None:
    """Change a user's role in the database.

    Example:
        python3 command.py role 1 --role=user

    """
    with sqlite3.connect(Config.DATABASE_URI) as conn:
        cur = conn.cursor()
        if not cur.execute("SELECT id FROM users WHERE id = ?", (user_id,)).fetchone():
            click.secho(f"User ID {user_id} not found", bg="red")
        else:
            cur.execute("UPDATE users SET role=? WHERE id=?", (role, user_id))
            conn.commit()
            click.secho("User role changed succefully", bg="green")


if __name__ == "__main__":
    cli()
