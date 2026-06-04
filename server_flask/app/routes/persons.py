"""Routes."""

from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING

from flask import Blueprint, Response, g, jsonify

from app.depends.depend import authorize, validize
from app.models.model import Person
from constants import BASE_PATH

if TYPE_CHECKING:
    import sqlite3

bp = Blueprint("persons", __name__, url_prefix="/persons")


@bp.get("/<int:person_id>")
def get_person(person_id: int) -> Response:
    """Retrieve an item from the database based on the provided item ID."""
    cur: sqlite3.Cursor = g.db.cursor()
    return jsonify(
        dict(
            cur.execute("SELECT * FROM persons WHERE id = ?", (person_id,)).fetchone(),
        ),
    ), 200


@bp.post("/")
@validize()
@authorize()
def post_person(json_data: Person) -> Response:
    """Replace a record in persons table."""
    # Загружаем резюме, получаем id кандидата, а также был ли он ранее загружен
    cur: sqlite3.Cursor = g.db.cursor()
    person = cur.execute(
        """
        SELECT id FROM persons WHERE
        surname=? AND firstname=? AND patronymic=? AND birthday=DATE(?)
        """,
        (
            json_data.surname,
            json_data.firstname,
            json_data.patronymic,
            json_data.birthday,
        ),
    ).fetchone()

    if not (cand_id := person[0] if person else None):
        data_dict = json_data.dict()
        data_dict["user_id"] = g.current_user["id"]
        data_dict["created"] = datetime.now(UTC)
        cand_id = cur.execute(
            "INSERT INTO persons ({}) VALUES ({})".format(  # noqa: S608
                ",".join(data_dict.keys()),
                ",".join(["?"] * len(data_dict)),
            ),
            tuple(data_dict.values()),
        ).lastrowid

        destination = Path(
            BASE_PATH,
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

        cur.execute(
            "UPDATE persons SET destination = ? WHERE id = ?",
            (str(destination), cand_id),
        )
        g.db.commit()
    return jsonify({"person_id": cand_id}), 201


@bp.patch("/<int:person_id>")
@validize()
@authorize()
def patch_person(person_id: int, json_data: Person) -> Response:
    """Replace a record in persons table."""
    # Загружаем резюме, получаем id кандидата, а также был ли он ранее загружен
    cur: sqlite3.Cursor = g.db.cursor()
    data = json_data.dict()
    data["user_id"] = g.current_user["id"]
    data["created"] = datetime.now(UTC)
    cur.execute(
        "UPDATE persons SET {} WHERE id = ?".format(  # noqa: S608
            ",".join(f"{k}=?" for k in data),
        ),
        (*data.values(), person_id),
    )
    g.db.commit()
    return "", 200
