"""Routes."""

import sqlite3
from datetime import UTC, datetime
from pathlib import Path
from typing import Literal

from flask import Blueprint, Response, current_app, g, jsonify

from app.depends.depend import authorize, validize
from app.models.model import Anketa, Person

bp = Blueprint("persons", __name__, url_prefix="/persons")


def add_person(cur: sqlite3.Cursor, json_data: Person) -> int | None:
    """Add a record in persons table."""
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
    if cand_id:
        return None

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
    return cand_id


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
    """Add a record in persons table."""
    cur: sqlite3.Cursor = g.db.cursor()
    cand_id = add_person(cur, json_data)
    g.db.commit()
    return jsonify({"person_id": cand_id}), 201


@bp.post("/json")
@validize()
@authorize()
def post_json_file(json_data: Anketa) -> tuple[Response, Literal[201]]:
    """Create a new person or updates an existing person from json."""
    cur: sqlite3.Cursor = g.db.cursor()

    cand_id = add_person(cur, Person.parse_obj(json_data))
    if cand_id:
        # Сохранение дополнительной информации о кандидате в БД
        items = {
            "documents": [
                {
                    "digits": json_data.digits,
                    "series": json_data.series,
                    "issue": json_data.issue,
                    "agency": json_data.agency,
                },
            ],
            "staffs": [
                {
                    "position": json_data.position,
                    "department": json_data.department,
                },
            ],
            "addresses": [
                {
                    "view": "Адрес проживания",
                    "address": json_data.valid_address,
                },
                {
                    "view": "Адрес регистрации",
                    "address": json_data.reg_address,
                },
            ],
            "contacts": [
                {
                    "view": "Телефон",
                    "contact": json_data.contact_phone,
                },
                {
                    "view": "Электронная почта",
                    "contact": json_data.email,
                },
            ],
            "educations": [
                education.dict()
                for education in json_data.education
                if json_data.education
            ],
            "workplaces": [
                workplace.dict()
                for workplace in json_data.experience
                if json_data.experience
            ],
            "previous": [
                prev.dict()
                for prev in json_data.name_was_changed
                if json_data.name_was_changed
            ],
            "affilations": [
                affilation.dict()
                for affilation in json_data.organizations
                if json_data.organizations
            ],
        }

        for table, contents in items.items():
            for content in contents:
                content["person_id"] = cand_id
                content["created"] = datetime.now(UTC)
                stmt = "INSERT INTO {} ({}) VALUES ({})".format(  # noqa: S608
                    table,
                    ",".join(content.keys()),
                    ",".join(["?"] * len(content)),
                )
                cur.execute(stmt, tuple(content.values()))
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
