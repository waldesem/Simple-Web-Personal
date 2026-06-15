"""Routes."""

from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING, Literal

from flask import Blueprint, Response, current_app, g, jsonify

from app.depends.depend import authorize, validize
from app.models.model import Person

if TYPE_CHECKING:
    import sqlite3

bp = Blueprint("persons", __name__, url_prefix="/persons")


@bp.get("/<int:person_id>")
def get_person(person_id: int) -> tuple[Response, Literal[200]]:
    """Retrieve a person from the database based on the provided ID."""
    cur: sqlite3.Cursor = g.db.cursor()
    person = cur.execute("SELECT * FROM persons WHERE id = ?", (person_id,)).fetchone()
    return jsonify(dict(person)), 200


@bp.post("/")
@validize()
@authorize()
def post_person(json_data: Person) -> tuple[Response, Literal[201]]:
    """Replace a record in persons table."""
    cur: sqlite3.Cursor = g.db.cursor()
    person = cur.execute(
        "SELECT id FROM persons WHERE\
            surname=? AND firstname=? AND patronymic=? AND birthday=?",
        (
            json_data.surname,
            json_data.firstname,
            json_data.patronymic,
            json_data.birthday,
        ),
    ).fetchone()

    cand_id = person[0] if person else None
    if not cand_id:
        data_dict = json_data.dict()
        data_dict["user_id"] = g.current_user["id"]
        data_dict["created"] = datetime.now(UTC)
        stmt = "INSERT INTO persons ({}) VALUES ({})".format(  # noqa: S608
            ",".join(data_dict.keys()),
            ",".join(["?"] * len(data_dict)),
        )
        cand_id = cur.execute(stmt, tuple(data_dict.values())).lastrowid

        if cand_id:
            destination = Path(
                current_app.config["BASE_PATH"],
                "Главный офис",
                json_data.surname[0],
                "{}-{} {} {}".format(
                    cand_id,
                    json_data.surname,
                    json_data.firstname,
                    json_data.patronymic or "",
                ).rstrip(),
            )
            destination.mkdir(parents=True, exist_ok=True)
            stmt = "UPDATE persons SET {} WHERE id = ?".format(  # noqa: S608
                ",".join(f"{k}=?" for k in data_dict),
            )
            cur.execute(stmt, (*data_dict.values(), cand_id))
            g.db.commit()
    return jsonify({"person_id": cand_id}), 201


@bp.patch("/<int:person_id>")
@validize()
@authorize()
def patch_person(person_id: int, json_data: Person) -> tuple[Literal[""], Literal[200]]:
    """Replace a record in persons table."""
    data = json_data.dict()
    data["user_id"] = g.current_user["id"]
    data["created"] = datetime.now(UTC)
    cur: sqlite3.Cursor = g.db.cursor()
    stmt = "UPDATE persons SET {} WHERE id = ?".format(  # noqa: S608
        ",".join(f"{k}=?" for k in data),
    )
    cur.execute(stmt, (*data.values(), person_id))
    g.db.commit()
    return "", 200
