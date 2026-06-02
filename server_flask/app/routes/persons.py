"""Routes."""

from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING

from flask import Blueprint, Response, g, jsonify, request

from app.depends.depend import auth_required
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
@auth_required()
def post_person() -> Response:
    """Replace a record in persons table."""
    # Загружаем резюме, получаем id кандидата, а также был ли он ранее загружен
    cur: sqlite3.Cursor = g.db.cursor()
    resume: dict = request.get_json()
    person = cur.execute(
        """
        SELECT id FROM persons WHERE
        surname=? AND firstname=? AND patronymic=? AND birthday=DATE(?)
        """,
        (
            resume["surname"],
            resume["firstname"],
            resume.get("patronymic", ""),
            resume["birthday"],
        ),
    ).fetchone()

    if not (cand_id := person[0] if person else None):
        resume.update(
            editable=False,
            user_id=g.current_user["id"],
            created=datetime.now(UTC),
        )
        cand_id = cur.execute(
            "INSERT INTO persons ({}) VALUES ({})".format(  # noqa: S608
                ",".join(resume.keys()),
                ",".join(["?"] * len(resume)),
            ),
            tuple(resume.values()),
        ).lastrowid

        destination = Path(
            BASE_PATH,
            "Главный офис",
            resume["surname"][0],
            "{}-{} {} {}".format(
                cand_id,
                resume["surname"],
                resume["firstname"],
                resume.get("patronymic", ""),
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
@auth_required()
def patch_person(person_id: int) -> Response:
    """Replace a record in persons table."""
    # Загружаем резюме, получаем id кандидата, а также был ли он ранее загружен
    cur: sqlite3.Cursor = g.db.cursor()
    resume: dict = request.get_json()
    resume["user_id"] = g.current_user["id"]
    cur.execute(
        "UPDATE persons SET {} WHERE id = ?".format(  # noqa: S608
            ",".join(f"{k}=?" for k in resume),
        ),
        (*resume.values(), person_id),
    )
    g.db.commit()
    return "", 200
